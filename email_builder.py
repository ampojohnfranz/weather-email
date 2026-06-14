def build_html(today_text, status, current_temp, current_condition, rain_prob, peak_rain_time, now):
    current_time = now.strftime("%I:%M %p")
    current_temp_display = f"{current_temp:.1f}°C" if current_temp is not None else "—"

    if rain_prob >= 40:
        status_color = "#38bdf8"
        status_label = "Rain Expected Today"
    else:
        status_color = "#4ade80"
        status_label = "Mostly Clear Today"

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:40px 20px;background-color:#0f172a;font-family:'Segoe UI',Arial,sans-serif;">

<table align="center" width="100%" cellpadding="0" cellspacing="0"
  style="max-width:600px;margin:0 auto;border-radius:12px;overflow:hidden;border:1px solid #1e293b;">

  <!-- HEADER -->
  <tr>
    <td style="background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);padding:32px 40px;">
      <div style="color:#38bdf8;font-size:11px;text-transform:uppercase;letter-spacing:2px;margin-bottom:6px;">
        {today_text}
      </div>
      <div style="color:#f1f5f9;font-size:22px;font-weight:700;letter-spacing:-0.5px;">
        Daily Weather Brief
      </div>
      <div style="color:#64748b;font-size:12px;margin-top:4px;">Cagayan de Oro · Automated Report</div>
    </td>
  </tr>

  <!-- AS OF NOW -->
  <tr>
    <td style="background-color:#1e293b;padding:24px 40px;border-top:1px solid #334155;">
      <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px;">
        As of {current_time}
      </div>
      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
          <td>
            <div style="font-size:36px;font-weight:700;color:#f97316;">{current_temp_display}</div>
            <div style="font-size:14px;color:#94a3b8;margin-top:4px;">{current_condition}</div>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- TODAY'S OUTLOOK -->
  <tr>
    <td style="background-color:#1e293b;padding:8px 40px 32px 40px;border-top:1px solid #0f172a;">
      <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px;">
        Expected Today
      </div>

      <table width="100%" cellpadding="0" cellspacing="0">
        <tr>

          <!-- Status -->
          <td width="32%" align="center"
            style="padding:20px 8px;background:#0f172a;border-radius:8px;">
            <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Status</div>
            <div style="font-size:13px;font-weight:700;color:{status_color};line-height:1.3;">{status_label}</div>
          </td>

          <td width="4%"></td>

          <!-- Rain Chance -->
          <td width="32%" align="center"
            style="padding:20px 8px;background:#0f172a;border-radius:8px;">
            <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Rain Chance</div>
            <div style="font-size:28px;font-weight:700;color:#38bdf8;">{rain_prob:.0f}%</div>
          </td>

          <td width="4%"></td>

          <!-- Peak Rain Time -->
          <td width="32%" align="center"
            style="padding:20px 8px;background:#0f172a;border-radius:8px;">
            <div style="font-size:10px;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">Expected At</div>
            <div style="font-size:16px;font-weight:700;color:#f1f5f9;margin-top:6px;">{peak_rain_time}</div>
          </td>

        </tr>
      </table>
    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="background-color:#0f172a;padding:16px 40px;border-top:1px solid #1e293b;">
      <div style="color:#334155;font-size:11px;">Automated System v2.0 · OpenWeather API</div>
    </td>
  </tr>

</table>
</body>
</html>"""