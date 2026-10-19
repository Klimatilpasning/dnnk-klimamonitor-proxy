"""Ugentlig mail til KP med klimamonitorens vurderede fund og systemstatus.

Indført 19/10-2026, så KP kan følge med under barslen (2/12-2026 - 10/3-2027)
uden at en pc står tændt. Alt kører online:
- GitHub Actions (.github/workflows/ugemail.yml) kører tools/sundhedstjek.py og
  POST'er resultatet til /send-ugemail. Fejler noget, sendes en alarmmail.
- En cloud-rutine hos Anthropic vurderer ugens fund (🟢/🟡/🔴) og lægger
  ugevurdering.json på branchen claude/ugevurdering. Mangler den (eller er den
  over 8 dage gammel), får mailen i stedet en sorteret liste uden vurdering.
- Mailen sendes via Brevo til DIGEST_EMAIL_TO (kp@dnnk.dk), samme opsætning
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


def byg_html(sundhed: list, vurdering: dict | None, raa: list, test: bool) -> tuple[str, str]:
    idag = datetime.now(timezone.utc).strftime("%d/%m-%Y")
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
        dele.append(f"<h2>Ugens fund ({_e(vurdering.get('periode'))})</h2>")
        if vurdering.get("opsummering"):
            dele.append(f"<p>{_e(vurdering['opsummering'])}</p>")
        for farve in ("groen", "gul"):
            valgt = [p for p in punkter if p.get("farve") == farve]
            if not valgt:
                continue
            titel = "Værd at forfølge" if farve == "groen" else "Værd et kig"
            li = "".join(
                f"<li>{FARVE[farve]} <a href=\"{_e(p.get('url'))}\">{_e(p.get('titel'))}</a>"
                f" <span style='color:#777'>- {_e(p.get('kilde'))}, {_e(p.get('dato'))}</span>"
                f"<br>{_e(p.get('begrundelse'))}</li>" for p in valgt)
            dele.append(f"<h3>{titel}</h3><ul>{li}</ul>")
        roede = sum(1 for p in punkter if p.get("farve") == "roed")
        if roede:
            dele.append(f"<p style='color:#777'>🔴 {roede} fund sorteret fra som støj.</p>")
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


async def send(emne: str, krop: str) -> dict:
    from scheduler import BREVO_API_KEY, DIGEST_EMAIL_TO, DIGEST_EMAIL_FROM, DIGEST_EMAIL_FROM_NAME
    if not BREVO_API_KEY:
        return {"sendt": False, "fejl": "BREVO_API_KEY er ikke sat på Render"}
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post("https://api.brevo.com/v3/smtp/email",
                         headers={"api-key": BREVO_API_KEY, "Content-Type": "application/json"},
                         json={"sender": {"name": DIGEST_EMAIL_FROM_NAME, "email": DIGEST_EMAIL_FROM},
                               "to": [{"email": DIGEST_EMAIL_TO}], "subject": emne, "htmlContent": krop})
    ok = r.status_code in (200, 201)
    return {"sendt": ok, "brevo_status": r.status_code, "til": DIGEST_EMAIL_TO,
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
        return await send(emne, krop)
    vurdering = await hent_vurdering(client)
    raa = [] if vurdering else await raa_fund(client)
    emne, krop = byg_html(sundhed, vurdering, raa, test)
    res = await send(emne, krop)
    return {**res, "emne": emne, "vurdering": bool(vurdering), "raa_fund": len(raa)}
