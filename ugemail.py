"""Ugentlig mail til KP med klimamonitorens vurderede fund og systemstatus.

Indført 19/10-2026, så KP kan følge med under barslen (2/12-2026 - 10/3-2027)
uden at en pc står tændt. Alt kører online:
- GitHub Actions (.github/workflows/ugemail.yml) kører tools/sundhedstjek.py og
  POST'er resultatet til /send-ugemail. Fejler noget, sendes en alarmmail.
- En cloud-rutine hos Anthropic vurderer ugens fund (🟢/🟡/🔴) og lægger
  ugevurdering.json på branchen claude/ugevurdering. Mangler den (eller er den
  over 8 dage gammel), får mailen i stedet en sorteret liste uden vurdering.
- Mailen sendes via Brevo til UGEMAIL_TO (kp@dnnk.dk, med systemstatus), og kun fundene til UGEMAIL_FUND_TO (sv@dnnk.dk), samme opsætning
  som den gamle digest.
"""
import asyncio
import html
import json
import os
from datetime import datetime, timedelta, timezone

import httpx

VURDERING_URL = ("https://raw.githubusercontent.com/Klimatilpasning/dnnk-klimamonitor-proxy/"
                 "claude/ugevurdering/ugevurdering.json")
MONITOR_URL = "https://klimatilpasning.github.io/dnnk-klimamonitor-proxy/"
FARVE = {"groen": "🟢", "gul": "🟡", "roed": "🔴"}


def _e(s) -> str:
    return html.escape(str(s or ""))


async def hent_vurdering(client) -> dict | None:
    """Ugens vurdering fra cloud-rutinen, eller None hvis den mangler/er for gammel."""
    try:
        r = await client.get(VURDERING_URL, params={"x": datetime.now().strftime("%Y%m%d%H")}, timeout=30)
        if r.status_code != 200:
            return None
        v = r.json()
        dato = datetime.fromisoformat((v.get("dato") or "1970-01-01")[:10]).date()
        if (datetime.now(timezone.utc).date() - dato).days > 8:
            return None
        return v
    except Exception as e:
        print(f"[ugemail] vurdering kunne ikke hentes: {e}")
        return None


async def raa_fund(client, dage: int = 10) -> list:
    """Reserve uden vurdering: ugens fund fra de kanaler, der dækker kommunerne."""
    import main as m
    graense = (datetime.now(timezone.utc) - timedelta(days=dage)).strftime("%Y-%m-%d")
    kald = {
        "Kommuneplaner": m.fetch_plandata(client), "Udbud": m.fetch_udbud_dk(client),
        "Kommuner (Ritzau)": m.fetch_ritzau(client), "Kommuner": m.fetch_kommunenyheder(client),
        "Politiske dagsordener": m.fetch_dagsordener(client),
    }
    res = await asyncio.gather(*kald.values(), return_exceptions=True)
    ud = []
    for gruppe, r in zip(kald, res):
        if isinstance(r, BaseException):
            continue
        for a in r:
            if (a.get("date") or "") < graense:
                continue
            if gruppe == "Politiske dagsordener" and (a.get("relevance") or 0) < 0.5:
                continue
            ud.append({**a, "gruppe": gruppe})
    ud.sort(key=lambda a: (a.get("relevance") or 0, a.get("date") or ""), reverse=True)
    return ud[:40]


def byg_html(sundhed: list, vurdering: dict | None, raa: list, test: bool, kun_fund: bool = False) -> tuple[str, str]:
    idag = datetime.now(timezone.utc).strftime("%d/%m-%Y")
    if kun_fund:
        sundhed = []
    fejl = [s for s in sundhed if not s.get("ok")]
    dele = []

    # Status
    if sundhed:
        status = ("✅ Alt kører" if not fejl else f"⚠️ {len(fejl)} advarsel(er)")
        linjer = "".join(
            f"<li>{'✅' if s.get('ok') else '⚠️'} <b>{_e(s.get('navn'))}</b>: {_e(s.get('tekst'))}</li>"
            for s in (fejl + [s for s in sundhed if s.get("ok")]))
        dele.append(f"<h2>Systemstatus: {status}</h2><ul>{linjer}</ul>")

    # Fund
    if vurdering:
        punkter = vurdering.get("punkter") or []
        groen = [p for p in punkter if p.get("farve") == "groen"]
        gul = [p for p in punkter if p.get("farve") == "gul"]
        roede = sum(1 for p in punkter if p.get("farve") == "roed")
        dele.append(f"<h2 style='margin-bottom:4px'>Ugens fund ({_e(vurdering.get('periode'))})</h2>")
        dele.append(f"<p style='color:#555;margin:0 0 10px'>{FARVE['groen']} {len(groen)} værd at forfølge &nbsp; "
                    f"{FARVE['gul']} {len(gul)} værd et kig &nbsp; 🔴 {roede} støj</p>")
        if vurdering.get("opsummering"):
            dele.append(f"<p style='background:#eef5f9;border-left:4px solid #1a4d6e;padding:10px 12px;margin:0 0 14px'>{_e(vurdering['opsummering'])}</p>")
        temaer = vurdering.get("temaer") or []
        if temaer:
            dele.append("<h3 style='color:#5b3a8c;border-bottom:2px solid #5b3a8c;padding-bottom:3px'>🧩 Temaer, der tegner sig</h3>"
                        "<p style='color:#777;font-size:12px;margin:0 0 6px'>Fund fra denne og tidligere uger, der hænger sammen og kunne blive til en temadag.</p>")
            for t in temaer:
                fund = t.get("fund") or []
                li = "".join(
                    f"<li style='margin:0 0 2px'><a href=\"{_e(f.get('url'))}\" style='color:#1a4d6e'>{_e(f.get('titel'))}</a>"
                    f" <span style='color:#777;font-size:12px'>- vurderet {_e(f.get('vurderet'))}</span></li>" for f in fund)
                dele.append(
                    f"<div style='border-left:4px solid #5b3a8c;background:#f8f5fc;padding:8px 12px;margin:0 0 10px'>"
                    f"<div style='font-weight:bold;color:#5b3a8c'>{_e(t.get('titel'))} <span style='font-weight:normal;color:#777;font-size:12px'>({len(fund)} fund)</span></div>"
                    f"<div style='font-size:14px;margin:4px 0'>{_e(t.get('vinkel'))}</div>"
                    + (f"<div style='font-size:14px;margin:0 0 4px'>{_vidensbank(t)}</div>" if _vidensbank(t) else "")
                    + f"<ul style='padding-left:18px;margin:4px 0 0;font-size:13px'>{li}</ul></div>")
        if groen:
            dele.append(f"<h3 style='color:#1b7a3a;border-bottom:2px solid #1b7a3a;padding-bottom:3px'>{FARVE['groen']} Værd at forfølge</h3>")
            for p in groen:
                dele.append(
                    f"<div style='border-left:4px solid #1b7a3a;background:#f6fbf7;padding:8px 12px;margin:0 0 8px'>"
                    f"<a href=\"{_e(p.get('url'))}\" style='font-weight:bold;color:#1a4d6e;text-decoration:none'>{_e(p.get('titel'))}</a>"
                    f"<div style='color:#777;font-size:12px;margin:2px 0 4px'>{_e(p.get('kilde'))} - {_e(p.get('dato'))}</div>"
                    + (f"<div style='font-size:14px;margin:0 0 3px'><b>Relevans:</b> {_e(p.get('relevans'))}</div>"
                       f"<div style='font-size:14px;margin:0 0 3px'><b>Mulighed:</b> {_e(p.get('mulighed'))}</div>"
                       if p.get("relevans") else f"<div style='font-size:14px'>{_e(p.get('begrundelse'))}</div>")
                    + (f"<div style='font-size:14px'>{_vidensbank(p)}</div>" if _vidensbank(p) else "")
                    + "</div>")
        if gul:
            dele.append(f"<h3 style='color:#a15c00;border-bottom:2px solid #d9a200;padding-bottom:3px'>{FARVE['gul']} Værd et kig</h3>"
                        "<p style='color:#777;font-size:12px;margin:0 0 6px'>Kun titel og kilde. Åbn klimamonitoren for begrundelse.</p>")
            li = "".join(
                f"<li style='margin:0 0 4px;font-size:14px'><a href=\"{_e(p.get('url'))}\" style='color:#1a4d6e'>{_e(p.get('titel'))}</a>"
                f" <span style='color:#777;font-size:12px'>- {_e(p.get('kilde'))}</span></li>" for p in gul)
            dele.append(f"<ul style='padding-left:18px;margin:0'>{li}</ul>")
    else:
        dele.append("<h2>Ugens fund (uden vurdering)</h2>"
                    "<p style='color:#a15c00'>Ugens vurdering mangler (cloud-rutinen har ikke leveret), "
                    "så her er de rå fund sorteret efter relevans.</p>")
        if raa:
            li = "".join(
                f"<li><a href=\"{_e(a.get('url'))}\">{_e(a.get('title'))}</a>"
                f" <span style='color:#777'>- {_e(a.get('gruppe'))}, {_e(a.get('date'))}</span></li>"
                for a in raa)
            dele.append(f"<ul>{li}</ul>")
        else:
            dele.append("<p>Ingen nye fund.</p>")

    emne = (("[TEST] " if test else "") + ("⚠️ " if fejl else "")
            + f"DNNK klimamonitor - uge {datetime.now(timezone.utc).isocalendar()[1]}")
    krop = f"""<!DOCTYPE html><html><body style="font-family:Arial,sans-serif;max-width:720px;margin:auto;color:#222;line-height:1.45">
<h1 style="color:#1a4d6e">DNNK klimamonitor - ugens overblik {idag}</h1>
{"<p style='background:#fff3cd;padding:8px'>Dette er en testmail.</p>" if test else ""}
{''.join(dele)}
<p style="color:#999;font-size:12px;border-top:1px solid #eee;padding-top:10px">
Sendt automatisk hver fredag fra GitHub Actions via Brevo. <a href="{MONITOR_URL}">Åbn klimamonitoren</a>.</p>
</body></html>"""
    return emne, krop


def _vidensbank(x: dict) -> str:
    """Vidensbank-linje: tekst + links (fra rutinens felter vidensbank og vidensbank_links)."""
    links = ", ".join(f"<a href=\"{_e(l.get('url'))}\">{_e(l.get('titel'))}</a>"
                      for l in (x.get("vidensbank_links") or []) if l.get("url"))
    tekst = _e(x.get("vidensbank") or "")
    if not (tekst or links):
        return ""
    return f"<b>Vidensbank:</b> {tekst}{' ' + links if links else ''}"


def _modtagere(raa: str) -> list:
    return [a.strip() for a in raa.split(",") if a.strip()]


async def send(emne: str, krop: str, alarm: bool = False, til_var: str = "UGEMAIL_TO") -> dict:
    from scheduler import BREVO_API_KEY, DIGEST_EMAIL_TO, DIGEST_EMAIL_FROM, DIGEST_EMAIL_FROM_NAME
    # UGEMAIL_TO = fuld mail med systemstatus (standard KP), UGEMAIL_FUND_TO = kun klimamonitor-fund (standard SV).
    # Begge kan have flere adresser, kommasepareret. Systemalarmen går kun til ALARM_EMAIL_TO (standard: DIGEST_EMAIL_TO).
    til = _modtagere(os.environ.get("ALARM_EMAIL_TO", DIGEST_EMAIL_TO) if alarm
                     else os.environ.get(til_var, "sv@dnnk.dk" if til_var == "UGEMAIL_FUND_TO" else "kp@dnnk.dk"))
    if not BREVO_API_KEY:
        return {"sendt": False, "fejl": "BREVO_API_KEY er ikke sat på Render"}
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post("https://api.brevo.com/v3/smtp/email",
                         headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
                         json={"sender": {"name": DIGEST_EMAIL_FROM_NAME, "email": DIGEST_EMAIL_FROM},
                               "to": [{"email": a} for a in til], "subject": emne, "htmlContent": krop})
    ok = r.status_code in (200, 201)
    return {"sendt": ok, "brevo_status": r.status_code, "til": til,
            **({} if ok else {"fejl": r.text[:300]})}


async def koer(client, sundhed: list, test: bool = False, kun_alarm: bool = False) -> dict:
    fejl = [s for s in sundhed if not s.get("ok")]
    if kun_alarm and not fejl:
        return {"sendt": False, "grund": "ingen fejl - ingen alarm"}
    if kun_alarm:
        emne = "⚠️ DNNK systemalarm: " + ", ".join(_e(s.get("navn")) for s in fejl)
        li = "".join(f"<li><b>{_e(s.get('navn'))}</b>: {_e(s.get('tekst'))}</li>" for s in fejl)
        krop = (f"<html><body style='font-family:Arial'><h2>{emne}</h2><ul>{li}</ul>"
                f"<p>Daglig kontrol fra GitHub Actions. Den samlede status kommer i fredagsmailen.</p></body></html>")
        return await send(emne, krop, alarm=True)
    vurdering = await hent_vurdering(client)
    raa = [] if vurdering else await raa_fund(client)
    emne, krop = byg_html(sundhed, vurdering, raa, test)
    res = await send(emne, krop)
    fund_emne, fund_krop = byg_html(sundhed, vurdering, raa, test, kun_fund=True)
    fund_res = await send(fund_emne, fund_krop, til_var="UGEMAIL_FUND_TO")
    return {**res, "fund_mail": fund_res, "emne": emne, "vurdering": bool(vurdering), "raa_fund": len(raa)}
