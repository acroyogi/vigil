def send_email(to_email, subject, message, override=False):
    try:
        msg = EmailMessage()
        msg["From"] = cfg.email["from"]
        msg["To"] = to_email
        msg["Subject"] = subject

        body = (
            f" {message.author.global_name}:.\n"
            f"Jump to message {message.jump_url}\n"
            f"{message.content}"
        )
        msg.add_header("Content-Type", "text/plain")
        msg.set_payload(body)
        if cfg.email["tls"] ^ override:
            with smtplib.SMTP(cfg.email["server"], cfg.email["port"]) as server:
                # server.set_debuglevel(True)
                server.starttls()
                self.loginSendQuit(server, to_email, msg)
        else:
            with smtplib.SMTP_SSL(cfg.email["server"], cfg.email["port"]) as server:
                loginSendQuit(server, to_email, msg)

        print(f"Email sent successfully to {to_email}")

send_email("3104879662@mypixmessages.com", "WEAPON ALERT", "ALERT: Weapon detected")