FROM python:3.10.0

ENV TOKEN = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ENV ALGORITHM="HS256"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30


ENV PATH_RESOURCES="resources"
ENV TYPE="service_account"
ENV PROJECT_ID="vision-aqc"
ENV PRIVATE_KEY_ID="4b151d65fbbdf0412411f12ee288907d1d68f067"
ENV PRIVATE_KEY='-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDlxS2hF3uSu8wr\nqOFdntFIzDZiQwsNbXv0tisXxqu/PfruOiYvM27Ib7MdUWZRBGPZNpVOePMsp05/\nTTCQjtUaHCEkXQ2sQoOKYjfZjeUQASH6+LVzxH/XgIFIqeDA2I5zqFSCtumiYd2e\n4fO8Oh7hQg+I3e67bV/pfvSUXQdzgPwXZ36Y1//ryiMG0WlopwJXxsXvqgOoQINY\nOlEULb29XDtwOgCLykxhu44ATaVPIKUA8PmIuGZk4mo23YFMoEHy3ILx9lMUKGNH\n4Q32BVIBKshYnGKhQPay7YMXklcOTjFzt+YuBkm7aUp8dPA8ATS8WUbRDYJwMLvE\n6meh02+XAgMBAAECggEAKyFeNVUBH0QdSTzEQRyk0HN06fEHzBd3IzJm2Gm0p4ts\n5PcJX+bZrso45xH2kNKwI3/5eud9Ti6Br6e/rAMDwYjyN68399PseTeCoFXgX6a2\nyDOTbA3AqaU3n3oz9D8yTkeUxYysQoz4WvCzHewTC9morNpsC8a2MFBifM8RrP54\nQjUz/QRobCjmMWZPYxwHSZvxCr/ptznjxL0u248AhVR3RbAJk7tdhEbaJEJdYuFT\nB3l3kqwmXS5aGZyI7UOsX8E3GdL6QclrNskZOffBXp0yx8kTwPDVEs2UpxddAtMR\ny2oJdDdea5DROJOunP5DNCr26KHU9LOhWCDnmFM7UQKBgQD3ExSh1DP6CbgKmeCF\nRfue/m1oV/wB9KaJh/v2lI9p5HyUN9p3d7STJeMvt3l5GW5gIYJw/MtcTIZxv1GE\naD15+uBXalTm+YpPwE3Urh5HGRAL8SNjOogjoxIm/R6ZyoAOF4SKwDQDhGFxg9LN\nw3ElgC3KzQnDMYflaRZOfd83rQKBgQDuEhG5Yx5ahlshPhveEjNO6+gQf8/gAgU1\nO49PtCUWyOm2aHUxWZHDurFnaueIdCbt/y1LUl9N6CY2pZsq7Vz2Qt3aebpkY3U6\nGzvStXcvEOvNUp/Wh+FcfwzF7VYlWcdMuDlqXXKpX8qxR3D/yb5grMm9cxS8fJ5O\nhLwsQnw80wKBgCYo8kTUS3rQyXYJsh2jY2t5DFjTTf7XVGllcUryQvwt5/fUcI+H\nE4KulVonUkGb5eo/ArCEurv0rccfr21t1CDk2IVnzNknrW8H2n2Arvh4LHxLsBWB\nUsl+RC11ZqaGGiUTCMuNR/tLFOm9XG+fQfhyxZ/O7zUQj1alVmalFja5AoGAU33y\nyVmBo63K9/WYQGGRrPP/BwpMFPugZ/LjZ8h92WfMzzQDJbOL82DeJq7PVIOnw3/i\nmq/gzKnF/RRHPt7P422/8IcQX3SiACbc7CDIE7GTgQahF9O/rXjBOgjqVV8PDlDt\nkegD9nKp21J6xroyEiWG+vIJK7Fos5DJjZwjhhECgYApjTYOzHaAs3Fhgv7ZyEN9\nc+TYl60yW3LU0yzMp+ZklB2JTdT4KbQdTSoOWPRMMcWfgrVMFc+rZxgkEYKoerjL\ncBtlax6phW0Sjm85l4EKF3qUxOO+agqlPxXYdhyLjo3209iDF9rmh+E02R3JXKmT\nz098BX5A8rSQSMgupA8Fkw==\n-----END PRIVATE KEY-----\n'
ENV CLIENT_EMAIL="vision-aqc@vision-aqc.iam.gserviceaccount.com"
ENV CLIENT_ID="101514877616574406482"
ENV AUTH_URI="https://accounts.google.com/o/oauth2/auth"
ENV TOKEN_URI="https://oauth2.googleapis.com/token"
ENV AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
ENV CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/vision-aqc%40vision-aqc.iam.gserviceaccount.com"

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

