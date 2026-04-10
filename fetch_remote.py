import urllib.request

try:
    url = "https://raw.githubusercontent.com/Mentorzx/Mentorzx/main/assets/profile/hero-banner.svg"
    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")
    with open("remote_svg.txt", "w") as f:
        f.write(html)
except Exception as e:
    with open("remote_svg.txt", "w") as f:
        f.write(str(e))
