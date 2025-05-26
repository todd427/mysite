import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()  # Likely where the cergmailt error occurs
server.login('todd427@gmail.com', 'mzlk ukri mykz fhwx')
server.sendmail('todd427@gmail.com', 'todd427@gmail.com', 'Semding a test email')
server.quit()
