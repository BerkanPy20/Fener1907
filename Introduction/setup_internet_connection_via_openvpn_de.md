<<<<<<< HEAD
# Anleitung Open-Vpn Verbindung auf einem Jetson Nano einrichten

## OpenVpn Zertifikat im Vorfeld erstellen
1. Anleitung auf der Intranet Seite vom Rechenzentrum der HS-Esslingen:
https://intranetportal.hs-esslingen.de/meine-hochschule/hochschul-services/rechenzentrum/zugang-zum-hochschulnetz-mobile-net-netzlaufwerke

2. Aus dem eigenem OpenVPN-HE Ordner (z.B.: C:\Users\vnnnnn\OpenVPN-HE) folgende Dateien auf einem USB Stick kopieren:

- he-ca.txt
- cert.txt
- key.txt

## Installation auf 

### Jetson Nano Orin starten und in WLAN einwählen

1. Unter Applications / Settings / Date & Time (ganz unten in der Liste) das aktuelle Datum und die Uhrzeit einstellen.
2. Unter Applications / Settings / Wi-Fi den WiFi Schalter einschalten und das W-Lan   VPN/WEB anwählen

### Setup VPN

1. Applications / Settings / Network öffnen
2. Hier beim VPN über die + Fläche eine neue OpenVPN Verbindung erstellen
3. Im Fenster Add VPN die erste Option OpenVPN (Compatible with OpenVPN Server) wählen
4. Im neuem Fenster im Reiter Identity folgende Eingaben machen

**Name:** Selbst genannte Name der Verbindung

**General:**
   - Gateway:  
    - openvpn-mia.hs-esslingen.de   (Mitarbeiter der HS-Esslingen)  
    - openvpn.hs-esslingen.de       (Studierender der HS-Esslingen)  

**Authentication:**

|  |  |
|---|---|
| Type:     |                        Password with Certificates (TLS)| 
| User name:           |        Hochschul account  (z.B. Max Schmid=mschmidt)| 
|Passwort:           |         Passwort vom Hochschul Account|
|CA certificate:      |      he-ca.txt   Zertifikat vom USB Stick kopieren|
|User certificate:     |    cert.txt   Zertifikat vom USB Stick kopieren|
|User private key:    |   key.txt   Zertifikat vom USB Stick kopieren|
|User key password : |Ihr Passwort vom Hochschul Account|

> [!WARNING]
> 1. Speichern sie ihr Passwort für den Hochschul Account nicht. 
> 2. Löschen sie die VPN-Konfiguration nach dam Workshop.

1. Mit dem Add  Button oben rechts die Eingabe bestätigen.
2. Die selbst erstellte OpenVpn Verbindung mit dem Schalter starten.
=======
# Guide: Setting up an OpenVPN connection on a Jetson Nano

## Pre-Setup: Create an OpenVPN Certificate
1. Follow the instructions on the IT Services portal of Esslingen University:
   [Intranet page for VPN setup](https://intranetportal.hs-esslingen.de/meine-hochschule/hochschul-services/rechenzentrum/zugang-zum-hochschulnetz-mobile-net-netzlaufwerke)

2. Copy the following files from your personal OpenVPN-HE folder (e.g., C:\Users\vnnnnn\OpenVPN-HE) to a USB stick:

   - he-ca.txt
   - cert.txt
   - key.txt

## Installation on the Jetson Nano

### Connect Jetson Nano Orin to Wi-Fi

1. Start the Jetson Nano Orin and connect to Wi-Fi.
2. Under **Applications / Settings / Date & Time** (at the bottom of the list), adjust the current date and time.
3. Go to **Applications / Settings / Wi-Fi**, switch on Wi-Fi, and select the WLAN network (e.g., VPN/WEB).

### VPN Setup

1. Open **Applications / Settings / Network**.
2. Click the "+" button to add a new OpenVPN connection.
3. In the **Add VPN** window, select the first option: **OpenVPN (Compatible with OpenVPN Server)**.
4. In the new window under the **Identity** tab, enter the following information:

**Name:** Enter a name of your choice for the connection.

**General:**

- **Gateway:**
   - For employees of Esslingen University: `openvpn-mia.hs-esslingen.de`
   - For students of Esslingen University: `openvpn.hs-esslingen.de`

**Authentication:**

| Setting              | Value                                               |
|----------------------|-----------------------------------------------------|
| **Type:**            | Password with Certificates (TLS)                    |
| **Username:**        | Your university account (e.g., Max Schmidt = mschmidt) |
| **Password:**        | Your university account password                    |
| **CA certificate:**  | Copy `he-ca.txt` from the USB stick                 |
| **User certificate:**| Copy `cert.txt` from the USB stick                  |
| **User private key:**| Copy `key.txt` from the USB stick                   |
| **User key password:**| Your university account password                   |

> **Warning:**
    > Do not save your university account password.
    > Delete the VPN configuration after the workshop.

5. Click **Add** (top right) to confirm the setup.
6. Switch on the OpenVPN connection you just created to activate it.
>>>>>>> feature/optimizations
