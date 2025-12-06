# src/ui/Expenses.py
import flet as ft
from datetime import datetime
from core import db
from core.theme import get_theme
from ui.nav_bar_buttom import create_page_with_nav


def get_clearbit_logo(domain: str) -> str:
    """Get brand logo URL from Clearbit API."""
    return f"https://logo.clearbit.com/{domain}"


def create_user_avatar(user_id: int, radius: int = 22, theme=None):
    """Create a user avatar based on their profile settings."""
    if theme is None:
        theme = get_theme()
    
    user_profile = db.get_user_profile(user_id)
    photo = user_profile.get("photo") if user_profile else None
    
    if photo and isinstance(photo, dict):
        photo_type = photo.get("type", "default")
        photo_value = photo.get("value")
        photo_bg = photo.get("bg")
        
        if photo_type == "avatar" and photo_value:
            # Emoji avatar
            return ft.Container(
                content=ft.Text(photo_value, size=radius * 0.8),
                width=radius * 2,
                height=radius * 2,
                bgcolor=photo_bg or theme.accent_primary,
                border_radius=radius,
                alignment=ft.alignment.center,
            )
        elif photo_type == "file" and photo_value:
            # Custom uploaded image
            return ft.Container(
                content=ft.Image(
                    src_base64=photo_value,
                    width=radius * 2 - 4,
                    height=radius * 2 - 4,
                    fit=ft.ImageFit.COVER,
                    border_radius=radius - 2,
                ),
                width=radius * 2,
                height=radius * 2,
                bgcolor="transparent",
                border_radius=radius,
                alignment=ft.alignment.center,
            )
    
    # Default avatar with user icon
    return ft.CircleAvatar(
        bgcolor=theme.accent_primary,
        content=ft.Icon(ft.Icons.PERSON, color="white", size=radius * 0.8),
        radius=radius,
    )


# Brand database for recognition - using Clearbit Logo API for clear, high-quality logos
BRAND_DATABASE = {
    # Shopping & E-commerce
    "amazon": {
        "icon": "a", "color": "#FF9900", "bg": "#232F3E", "text": "white",
        "logo": get_clearbit_logo("amazon.com")
    },
    "shopee": {
        "icon": "🛒", "color": "#EE4D2D", "bg": "#EE4D2D", "text": "white",
        "logo": get_clearbit_logo("shopee.com")
    },
    "lazada": {
        "icon": "L", "color": "#0F146D", "bg": "#0F146D", "text": "white",
        "logo": get_clearbit_logo("lazada.com")
    },
    "zalora": {
        "icon": "Z", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("zalora.com")
    },
    "ebay": {
        "icon": "e", "color": "#E53238", "bg": "#FFFFFF", "text": "#E53238",
        "logo": get_clearbit_logo("ebay.com")
    },
    "alibaba": {
        "icon": "A", "color": "#FF6A00", "bg": "#FF6A00", "text": "white",
        "logo": get_clearbit_logo("alibaba.com")
    },
    "temu": {
        "icon": "T", "color": "#F97316", "bg": "#F97316", "text": "white",
        "logo": get_clearbit_logo("temu.com")
    },
    "shein": {
        "icon": "S", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("shein.com")
    },
    
    # Food & Restaurants
    "mcdonalds": {
        "icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C",
        "logo": get_clearbit_logo("mcdonalds.com")
    },
    "mcdonald's": {
        "icon": "M", "color": "#FFC72C", "bg": "#DA291C", "text": "#FFC72C",
        "logo": get_clearbit_logo("mcdonalds.com")
    },
    "starbucks": {
        "icon": "☕", "color": "#00704A", "bg": "#00704A", "text": "white",
        "logo": get_clearbit_logo("starbucks.com")
    },
    "jollibee": {
        "icon": "🐝", "color": "#E31837", "bg": "#E31837", "text": "white",
        "logo": get_clearbit_logo("jollibee.com.ph")
    },
    "kfc": {
        "icon": "🍗", "color": "#F40027", "bg": "#F40027", "text": "white",
        "logo": get_clearbit_logo("kfc.com")
    },
    "burger king": {
        "icon": "🍔", "color": "#FF8732", "bg": "#502314", "text": "#FF8732",
        "logo": get_clearbit_logo("bk.com")
    },
    "pizza hut": {
        "icon": "🍕", "color": "#E31837", "bg": "#E31837", "text": "white",
        "logo": get_clearbit_logo("pizzahut.com")
    },
    "dominos": {
        "icon": "🍕", "color": "#006491", "bg": "#006491", "text": "white",
        "logo": get_clearbit_logo("dominos.com")
    },
    "domino's": {
        "icon": "🍕", "color": "#006491", "bg": "#006491", "text": "white",
        "logo": get_clearbit_logo("dominos.com")
    },
    "subway": {
        "icon": "🥪", "color": "#008C15", "bg": "#FFC600", "text": "#008C15",
        "logo": get_clearbit_logo("subway.com")
    },
    "dunkin": {
        "icon": "🍩", "color": "#FF671F", "bg": "#FF671F", "text": "white",
        "logo": get_clearbit_logo("dunkindonuts.com")
    },
    "chowking": {
        "icon": "🥡", "color": "#E31837", "bg": "#E31837", "text": "white",
        "logo": get_clearbit_logo("chowkingdelivery.com")
    },
    "greenwich": {
        "icon": "🍕", "color": "#006B3F", "bg": "#006B3F", "text": "white",
        "logo": get_clearbit_logo("greenwichdelivery.com")
    },
    "mang inasal": {
        "icon": "🍗", "color": "#FDB813", "bg": "#FDB813", "text": "#1E1E1E",
        "logo": get_clearbit_logo("manginasal.com")
    },
    "yellow cab": {
        "icon": "🍕", "color": "#FFD100", "bg": "#000000", "text": "#FFD100",
        "logo": get_clearbit_logo("yellowcabpizza.com")
    },
    "shakeys": {
        "icon": "🍕", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": get_clearbit_logo("shakeyspizza.ph")
    },
    "shakey's": {
        "icon": "🍕", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": get_clearbit_logo("shakeyspizza.ph")
    },
    "wendy's": {
        "icon": "W", "color": "#E2164B", "bg": "#E2164B", "text": "white",
        "logo": get_clearbit_logo("wendys.com")
    },
    "wendys": {
        "icon": "W", "color": "#E2164B", "bg": "#E2164B", "text": "white",
        "logo": get_clearbit_logo("wendys.com")
    },
    "taco bell": {
        "icon": "🌮", "color": "#702082", "bg": "#702082", "text": "white",
        "logo": get_clearbit_logo("tacobell.com")
    },
    "chipotle": {
        "icon": "🌯", "color": "#441500", "bg": "#441500", "text": "white",
        "logo": get_clearbit_logo("chipotle.com")
    },
    "popeyes": {
        "icon": "🍗", "color": "#FF6700", "bg": "#FF6700", "text": "white",
        "logo": get_clearbit_logo("popeyes.com")
    },
    "krispy kreme": {
        "icon": "🍩", "color": "#00873C", "bg": "#00873C", "text": "white",
        "logo": get_clearbit_logo("krispykreme.com")
    },
    "tim hortons": {
        "icon": "☕", "color": "#C8102E", "bg": "#C8102E", "text": "white",
        "logo": get_clearbit_logo("timhortons.com")
    },
    "papa johns": {
        "icon": "🍕", "color": "#008145", "bg": "#008145", "text": "white",
        "logo": get_clearbit_logo("papajohns.com")
    },
    
    # Tech & Electronics
    "apple": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("apple.com")
    },
    "ipad": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("apple.com")
    },
    "iphone": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("apple.com")
    },
    "macbook": {
        "icon": "", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("apple.com")
    },
    "airpods": {
        "icon": "🎧", "color": "#555555", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("apple.com")
    },
    "samsung": {
        "icon": "S", "color": "#1428A0", "bg": "#1428A0", "text": "white",
        "logo": get_clearbit_logo("samsung.com")
    },
    "galaxy": {
        "icon": "S", "color": "#1428A0", "bg": "#1428A0", "text": "white",
        "logo": get_clearbit_logo("samsung.com")
    },
    "google": {
        "icon": "G", "color": "#4285F4", "bg": "#FFFFFF", "text": "#4285F4",
        "logo": get_clearbit_logo("google.com")
    },
    "pixel": {
        "icon": "G", "color": "#4285F4", "bg": "#FFFFFF", "text": "#4285F4",
        "logo": get_clearbit_logo("google.com")
    },
    "microsoft": {
        "icon": "⊞", "color": "#00A4EF", "bg": "#737373", "text": "white",
        "logo": get_clearbit_logo("microsoft.com")
    },
    "xbox": {
        "icon": "X", "color": "#107C10", "bg": "#107C10", "text": "white",
        "logo": get_clearbit_logo("xbox.com")
    },
    "sony": {
        "icon": "S", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("sony.com")
    },
    "playstation": {
        "icon": "P", "color": "#003791", "bg": "#003791", "text": "white",
        "logo": get_clearbit_logo("playstation.com")
    },
    "ps5": {
        "icon": "P", "color": "#003791", "bg": "#003791", "text": "white",
        "logo": get_clearbit_logo("playstation.com")
    },
    "nintendo": {
        "icon": "N", "color": "#E60012", "bg": "#E60012", "text": "white",
        "logo": get_clearbit_logo("nintendo.com")
    },
    "dell": {
        "icon": "D", "color": "#007DB8", "bg": "#007DB8", "text": "white",
        "logo": get_clearbit_logo("dell.com")
    },
    "hp": {
        "icon": "hp", "color": "#0096D6", "bg": "#0096D6", "text": "white",
        "logo": get_clearbit_logo("hp.com")
    },
    "lenovo": {
        "icon": "L", "color": "#E2231A", "bg": "#E2231A", "text": "white",
        "logo": get_clearbit_logo("lenovo.com")
    },
    "asus": {
        "icon": "A", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("asus.com")
    },
    "acer": {
        "icon": "A", "color": "#83B81A", "bg": "#83B81A", "text": "white",
        "logo": get_clearbit_logo("acer.com")
    },
    "huawei": {
        "icon": "H", "color": "#FF0000", "bg": "#FF0000", "text": "white",
        "logo": get_clearbit_logo("huawei.com")
    },
    "xiaomi": {
        "icon": "Mi", "color": "#FF6900", "bg": "#FF6900", "text": "white",
        "logo": get_clearbit_logo("mi.com")
    },
    "oppo": {
        "icon": "O", "color": "#1BA784", "bg": "#1BA784", "text": "white",
        "logo": get_clearbit_logo("oppo.com")
    },
    "vivo": {
        "icon": "V", "color": "#415FFF", "bg": "#415FFF", "text": "white",
        "logo": get_clearbit_logo("vivo.com")
    },
    "realme": {
        "icon": "R", "color": "#F5C700", "bg": "#F5C700", "text": "#1E1E1E",
        "logo": get_clearbit_logo("realme.com")
    },
    "jbl": {
        "icon": "JBL", "color": "#FF6600", "bg": "#FF6600", "text": "white",
        "logo": get_clearbit_logo("jbl.com")
    },
    "bose": {
        "icon": "B", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("bose.com")
    },
    "beats": {
        "icon": "b", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": get_clearbit_logo("beatsbydre.com")
    },
    "logitech": {
        "icon": "L", "color": "#00B8FC", "bg": "#00B8FC", "text": "white",
        "logo": get_clearbit_logo("logitech.com")
    },
    "razer": {
        "icon": "R", "color": "#44D62C", "bg": "#000000", "text": "#44D62C",
        "logo": get_clearbit_logo("razer.com")
    },
    "gopro": {
        "icon": "G", "color": "#00A0D6", "bg": "#00A0D6", "text": "white",
        "logo": get_clearbit_logo("gopro.com")
    },
    "canon": {
        "icon": "C", "color": "#BC0024", "bg": "#BC0024", "text": "white",
        "logo": get_clearbit_logo("canon.com")
    },
    "nikon": {
        "icon": "N", "color": "#F6CE13", "bg": "#F6CE13", "text": "#1E1E1E",
        "logo": get_clearbit_logo("nikon.com")
    },
    "fujifilm": {
        "icon": "F", "color": "#ED1A3A", "bg": "#ED1A3A", "text": "white",
        "logo": get_clearbit_logo("fujifilm.com")
    },
    
    # Finance & Payment
    "mastercard": {
        "icon": "●●", "color": "#EB001B", "bg": "#FF5F00", "text": "white",
        "logo": get_clearbit_logo("mastercard.com")
    },
    "visa": {
        "icon": "V", "color": "#1A1F71", "bg": "#1A1F71", "text": "white",
        "logo": get_clearbit_logo("visa.com")
    },
    "paypal": {
        "icon": "P", "color": "#003087", "bg": "#003087", "text": "white",
        "logo": get_clearbit_logo("paypal.com")
    },
    "gcash": {
        "icon": "G", "color": "#007DFE", "bg": "#007DFE", "text": "white",
        "logo": get_clearbit_logo("gcash.com")
    },
    "maya": {
        "icon": "M", "color": "#00D66C", "bg": "#00D66C", "text": "white",
        "logo": get_clearbit_logo("maya.ph")
    },
    "paymaya": {
        "icon": "M", "color": "#00D66C", "bg": "#00D66C", "text": "white",
        "logo": get_clearbit_logo("maya.ph")
    },
    "bpi": {
        "icon": "B", "color": "#9E1B34", "bg": "#9E1B34", "text": "white",
        "logo": get_clearbit_logo("bpi.com.ph")
    },
    "bdo": {
        "icon": "B", "color": "#003478", "bg": "#003478", "text": "white",
        "logo": get_clearbit_logo("bdo.com.ph")
    },
    "metrobank": {
        "icon": "M", "color": "#003DA5", "bg": "#003DA5", "text": "white",
        "logo": get_clearbit_logo("metrobank.com.ph")
    },
    "landbank": {
        "icon": "L", "color": "#006400", "bg": "#006400", "text": "white",
        "logo": get_clearbit_logo("landbank.com")
    },
    "unionbank": {
        "icon": "U", "color": "#FF6600", "bg": "#FF6600", "text": "white",
        "logo": get_clearbit_logo("unionbankph.com")
    },
    
    # Streaming & Entertainment
    "netflix": {
        "icon": "N", "color": "#E50914", "bg": "#000000", "text": "#E50914",
        "logo": get_clearbit_logo("netflix.com")
    },
    "spotify": {
        "icon": "♪", "color": "#1DB954", "bg": "#191414", "text": "#1DB954",
        "logo": get_clearbit_logo("spotify.com")
    },
    "youtube": {
        "icon": "▶", "color": "#FF0000", "bg": "#282828", "text": "#FF0000",
        "logo": get_clearbit_logo("youtube.com")
    },
    "youtube premium": {
        "icon": "▶", "color": "#FF0000", "bg": "#282828", "text": "#FF0000",
        "logo": get_clearbit_logo("youtube.com")
    },
    "disney": {
        "icon": "D", "color": "#113CCF", "bg": "#040814", "text": "white",
        "logo": get_clearbit_logo("disneyplus.com")
    },
    "disney+": {
        "icon": "D", "color": "#113CCF", "bg": "#040814", "text": "white",
        "logo": get_clearbit_logo("disneyplus.com")
    },
    "hbo": {
        "icon": "H", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("hbomax.com")
    },
    "hulu": {
        "icon": "H", "color": "#1CE783", "bg": "#1CE783", "text": "#1E1E1E",
        "logo": get_clearbit_logo("hulu.com")
    },
    "amazon prime": {
        "icon": "P", "color": "#00A8E1", "bg": "#232F3E", "text": "white",
        "logo": get_clearbit_logo("primevideo.com")
    },
    "prime video": {
        "icon": "P", "color": "#00A8E1", "bg": "#232F3E", "text": "white",
        "logo": get_clearbit_logo("primevideo.com")
    },
    "twitch": {
        "icon": "T", "color": "#9146FF", "bg": "#9146FF", "text": "white",
        "logo": get_clearbit_logo("twitch.tv")
    },
    "steam": {
        "icon": "S", "color": "#1B2838", "bg": "#1B2838", "text": "white",
        "logo": get_clearbit_logo("steampowered.com")
    },
    "epic games": {
        "icon": "E", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("epicgames.com")
    },
    
    # Transport
    "grab": {
        "icon": "G", "color": "#00B14F", "bg": "#00B14F", "text": "white",
        "logo": get_clearbit_logo("grab.com")
    },
    "grabfood": {
        "icon": "G", "color": "#00B14F", "bg": "#00B14F", "text": "white",
        "logo": get_clearbit_logo("grab.com")
    },
    "uber": {
        "icon": "U", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("uber.com")
    },
    "angkas": {
        "icon": "A", "color": "#F16521", "bg": "#F16521", "text": "white",
        "logo": get_clearbit_logo("angkas.com")
    },
    "foodpanda": {
        "icon": "🐼", "color": "#D70F64", "bg": "#D70F64", "text": "white",
        "logo": get_clearbit_logo("foodpanda.com")
    },
    "lalamove": {
        "icon": "L", "color": "#F26722", "bg": "#F26722", "text": "white",
        "logo": get_clearbit_logo("lalamove.com")
    },
    "shell": {
        "icon": "🐚", "color": "#FBCE07", "bg": "#DD1D21", "text": "#FBCE07",
        "logo": get_clearbit_logo("shell.com")
    },
    "petron": {
        "icon": "P", "color": "#1E4D8C", "bg": "#1E4D8C", "text": "white",
        "logo": get_clearbit_logo("petron.com")
    },
    "caltex": {
        "icon": "★", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": get_clearbit_logo("caltex.com")
    },
    "phoenix": {
        "icon": "P", "color": "#FF6600", "bg": "#FF6600", "text": "white",
        "logo": get_clearbit_logo("phoenixfuels.ph")
    },
    
    # Utilities
    "meralco": {
        "icon": "⚡", "color": "#FF6B00", "bg": "#FF6B00", "text": "white",
        "logo": get_clearbit_logo("meralco.com.ph")
    },
    "pldt": {
        "icon": "P", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": get_clearbit_logo("pldthome.com")
    },
    "globe": {
        "icon": "G", "color": "#0056A3", "bg": "#0056A3", "text": "white",
        "logo": get_clearbit_logo("globe.com.ph")
    },
    "smart": {
        "icon": "S", "color": "#00913A", "bg": "#00913A", "text": "white",
        "logo": get_clearbit_logo("smart.com.ph")
    },
    "maynilad": {
        "icon": "M", "color": "#0072CE", "bg": "#0072CE", "text": "white",
        "logo": get_clearbit_logo("mayniladwater.com.ph")
    },
    "manila water": {
        "icon": "M", "color": "#003DA5", "bg": "#003DA5", "text": "white",
        "logo": get_clearbit_logo("manilawater.com")
    },
    "converge": {
        "icon": "C", "color": "#FF6600", "bg": "#FF6600", "text": "white",
        "logo": get_clearbit_logo("convergeict.com")
    },
    
    # Retail & Supermarkets
    "sm": {
        "icon": "SM", "color": "#003DA5", "bg": "#003DA5", "text": "white",
        "logo": get_clearbit_logo("smsupermalls.com")
    },
    "sm supermarket": {
        "icon": "SM", "color": "#003DA5", "bg": "#003DA5", "text": "white",
        "logo": get_clearbit_logo("smsupermarket.com")
    },
    "robinsons": {
        "icon": "R", "color": "#00529B", "bg": "#00529B", "text": "white",
        "logo": get_clearbit_logo("robinsonsmalls.com")
    },
    "puregold": {
        "icon": "P", "color": "#FFD700", "bg": "#FFD700", "text": "#1E1E1E",
        "logo": get_clearbit_logo("puregold.com.ph")
    },
    "savemore": {
        "icon": "S", "color": "#00529B", "bg": "#00529B", "text": "white",
        "logo": get_clearbit_logo("savemore.com.ph")
    },
    "mercury drug": {
        "icon": "M", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": get_clearbit_logo("mercurydrug.com")
    },
    "watsons": {
        "icon": "W", "color": "#00A651", "bg": "#00A651", "text": "white",
        "logo": get_clearbit_logo("watsons.com.ph")
    },
    "7-eleven": {
        "icon": "7", "color": "#00703C", "bg": "#00703C", "text": "white",
        "logo": get_clearbit_logo("7-eleven.com")
    },
    "7eleven": {
        "icon": "7", "color": "#00703C", "bg": "#00703C", "text": "white",
        "logo": get_clearbit_logo("7-eleven.com")
    },
    "ministop": {
        "icon": "M", "color": "#003DA5", "bg": "#003DA5", "text": "white",
        "logo": get_clearbit_logo("ministop.com.ph")
    },
    "family mart": {
        "icon": "F", "color": "#00703C", "bg": "#00703C", "text": "white",
        "logo": get_clearbit_logo("family.co.jp")
    },
    
    # Fashion & Apparel
    "uniqlo": {
        "icon": "U", "color": "#FF0000", "bg": "#FFFFFF", "text": "#FF0000",
        "logo": get_clearbit_logo("uniqlo.com")
    },
    "h&m": {
        "icon": "H&M", "color": "#E50010", "bg": "#FFFFFF", "text": "#E50010",
        "logo": get_clearbit_logo("hm.com")
    },
    "zara": {
        "icon": "Z", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("zara.com")
    },
    "nike": {
        "icon": "✓", "color": "#111111", "bg": "#111111", "text": "white",
        "logo": get_clearbit_logo("nike.com")
    },
    "adidas": {
        "icon": "⫿", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("adidas.com")
    },
    "puma": {
        "icon": "P", "color": "#E31937", "bg": "#E31937", "text": "white",
        "logo": get_clearbit_logo("puma.com")
    },
    "new balance": {
        "icon": "NB", "color": "#CF0A2C", "bg": "#CF0A2C", "text": "white",
        "logo": get_clearbit_logo("newbalance.com")
    },
    "converse": {
        "icon": "★", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("converse.com")
    },
    "vans": {
        "icon": "V", "color": "#C41230", "bg": "#C41230", "text": "white",
        "logo": get_clearbit_logo("vans.com")
    },
    "skechers": {
        "icon": "S", "color": "#0033A0", "bg": "#0033A0", "text": "white",
        "logo": get_clearbit_logo("skechers.com")
    },
    "under armour": {
        "icon": "UA", "color": "#1D1D1D", "bg": "#1D1D1D", "text": "white",
        "logo": get_clearbit_logo("underarmour.com")
    },
    "gap": {
        "icon": "GAP", "color": "#1E3A5F", "bg": "#1E3A5F", "text": "white",
        "logo": get_clearbit_logo("gap.com")
    },
    "levis": {
        "icon": "L", "color": "#C41230", "bg": "#C41230", "text": "white",
        "logo": get_clearbit_logo("levi.com")
    },
    "levi's": {
        "icon": "L", "color": "#C41230", "bg": "#C41230", "text": "white",
        "logo": get_clearbit_logo("levi.com")
    },
    "gucci": {
        "icon": "G", "color": "#1B4D3E", "bg": "#1B4D3E", "text": "white",
        "logo": get_clearbit_logo("gucci.com")
    },
    "louis vuitton": {
        "icon": "LV", "color": "#8B6914", "bg": "#8B6914", "text": "white",
        "logo": get_clearbit_logo("louisvuitton.com")
    },
    "lv": {
        "icon": "LV", "color": "#8B6914", "bg": "#8B6914", "text": "white",
        "logo": get_clearbit_logo("louisvuitton.com")
    },
    "chanel": {
        "icon": "C", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("chanel.com")
    },
    "prada": {
        "icon": "P", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("prada.com")
    },
    "crocs": {
        "icon": "C", "color": "#00A651", "bg": "#00A651", "text": "white",
        "logo": get_clearbit_logo("crocs.com")
    },
    
    # Coffee & Cafes
    "coffee bean": {
        "icon": "☕", "color": "#6B3A1E", "bg": "#6B3A1E", "text": "white",
        "logo": get_clearbit_logo("coffeebean.com")
    },
    "bo's coffee": {
        "icon": "☕", "color": "#003DA5", "bg": "#003DA5", "text": "white",
        "logo": get_clearbit_logo("bfranchising.com")
    },
    
    # Software & Services
    "adobe": {
        "icon": "A", "color": "#FF0000", "bg": "#FF0000", "text": "white",
        "logo": get_clearbit_logo("adobe.com")
    },
    "dropbox": {
        "icon": "D", "color": "#0061FF", "bg": "#0061FF", "text": "white",
        "logo": get_clearbit_logo("dropbox.com")
    },
    "slack": {
        "icon": "S", "color": "#4A154B", "bg": "#4A154B", "text": "white",
        "logo": get_clearbit_logo("slack.com")
    },
    "zoom": {
        "icon": "Z", "color": "#2D8CFF", "bg": "#2D8CFF", "text": "white",
        "logo": get_clearbit_logo("zoom.us")
    },
    "notion": {
        "icon": "N", "color": "#000000", "bg": "#000000", "text": "white",
        "logo": get_clearbit_logo("notion.so")
    },
    "canva": {
        "icon": "C", "color": "#00C4CC", "bg": "#00C4CC", "text": "white",
        "logo": get_clearbit_logo("canva.com")
    },
    "github": {
        "icon": "G", "color": "#181717", "bg": "#181717", "text": "white",
        "logo": get_clearbit_logo("github.com")
    },
    "figma": {
        "icon": "F", "color": "#F24E1E", "bg": "#F24E1E", "text": "white",
        "logo": get_clearbit_logo("figma.com")
    },
}


def get_brand_info(text: str):
    """Get brand info from text."""
    text_lower = text.lower()
    for brand, info in BRAND_DATABASE.items():
        if brand in text_lower:
            return info
    return None


def create_expense_item(brand_text: str, date: str, amount: float, on_click=None, theme=None, account_name: str = None):
    """Creates a modern expense item row with real brand logos and theme support."""
    # Get theme if not provided
    if theme is None:
        theme = get_theme()
    
    # Format amount and determine colors
    is_expense = amount < 0
    amount_str = f"-₱{abs(amount):,.2f}" if is_expense else f"+₱{amount:,.2f}"
    
    # Theme-aware amount colors
    if is_expense:
        amount_color = "#EF4444"  # Red
        amount_bg = "#3D1515" if theme.is_dark else "#FEE2E2"
    else:
        amount_color = "#10B981"  # Green  
        amount_bg = "#0D3D2E" if theme.is_dark else "#D1FAE5"
    
    # Get brand info
    brand_info = get_brand_info(brand_text)
    
    if brand_info:
        # Check if we have a logo URL
        if "logo" in brand_info and brand_info["logo"]:
            # Use real brand logo image with clean white background
            icon_container = ft.Container(
                content=ft.Container(
                    content=ft.Image(
                        src=brand_info["logo"],
                        width=32,
                        height=32,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Text(
                            brand_info["icon"],
                            size=18,
                            color=brand_info.get("text", "white"),
                            text_align=ft.TextAlign.CENTER,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ),
                    width=40,
                    height=40,
                    border_radius=8,
                    bgcolor="#FFFFFF",  # Clean white background for logo
                    alignment=ft.alignment.center,
                ),
                width=48,
                height=48,
                border_radius=12,
                bgcolor="#FFFFFF",  # Outer container also white
                alignment=ft.alignment.center,
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=8,
                    color="#00000020",
                    offset=ft.Offset(0, 2),
                ),
            )
        else:
            # Fallback to text icon
            icon_container = ft.Container(
                content=ft.Text(
                    brand_info["icon"],
                    size=20,
                    color=brand_info.get("text", "white"),
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                ),
                width=48,
                height=48,
                border_radius=14,
                bgcolor=brand_info["bg"],
                alignment=ft.alignment.center,
            )
    else:
        # Default icon for unknown brands
        icon_container = ft.Container(
            content=ft.Icon(ft.Icons.PAYMENTS, color="white", size=22),
            width=48,
            height=48,
            border_radius=14,
            bgcolor="#374151",
            alignment=ft.alignment.center,
        )
    
    # Amount badge with rounded pill shape
    amount_badge = ft.Container(
        content=ft.Text(
            amount_str,
            size=12,
            weight=ft.FontWeight.W_600,
            color=amount_color,
        ),
        padding=ft.padding.symmetric(horizontal=14, vertical=7),
        border_radius=18,
        bgcolor=amount_bg,
    )
    
    # Account badge
    account_badge = ft.Row([
        ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=10, color=theme.accent_primary),
        ft.Text(account_name or "Cash", size=10, color=theme.accent_primary, weight=ft.FontWeight.W_500),
    ], spacing=3, tight=True) if account_name else ft.Container()
    
    return ft.Container(
        content=ft.Row(
            controls=[
                icon_container,
                ft.Container(width=12),
                # Title and date column
                ft.Column(
                    controls=[
                        ft.Text(
                            brand_text,
                            size=15,
                            weight=ft.FontWeight.W_500,
                            color=theme.text_primary,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                        ),
                        ft.Text(
                            date,
                            size=12,
                            color=theme.text_muted,
                        ),
                    ],
                    spacing=3,
                    expand=True,
                ),
                # Amount and Account badge - fixed position right side
                ft.Column([
                    amount_badge,
                    account_badge,
                ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.END),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=12, horizontal=8),
        on_click=on_click,
        ink=True,
        border_radius=14,
        bgcolor=theme.bg_card if theme else "#1F2937",
    )


def create_expenses_view(page: ft.Page, state: dict, toast, show_home, show_wallet, show_profile, show_add_expense):
    """
    Creates the Expenses page view with modern UI and smooth animations.
    """
    
    expenses_list = ft.Column(spacing=6)
    
    # Initialize selected account in state if not exists
    if "selected_account_id" not in state:
        state["selected_account_id"] = None  # None means use primary account
    
    def format_date(date_str: str) -> str:
        """Format date string to display format (e.g., Sept 09, 2022)."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%b %d, %Y")
        except:
            return date_str
    
    def load_expenses():
        """Load and display all expenses with theme support."""
        theme = get_theme()
        expenses_list.controls.clear()
        rows = db.select_expenses_by_user(state["user_id"])
        
        # Cache account names for efficiency
        account_cache = {}
        def get_account_name(acc_id):
            if acc_id is None:
                return None
            if acc_id not in account_cache:
                acc = db.get_account_by_id(acc_id, state["user_id"])
                account_cache[acc_id] = acc[1] if acc else None
            return account_cache[acc_id]
        
        for r in rows:
            # Unpack with account_id (position 6)
            eid, uid, amt, cat, dsc, dtt, acc_id = r[:7]
            display_name = dsc if dsc else cat
            acc_name = get_account_name(acc_id)
            
            expenses_list.controls.append(
                create_expense_item(
                    brand_text=display_name,
                    date=format_date(dtt),
                    amount=-amt,  # Expenses are negative
                    theme=theme,
                    account_name=acc_name,
                )
            )
        
        if not rows:
            expenses_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Icon(ft.Icons.RECEIPT_LONG, color=theme.text_muted, size=56),
                                width=100,
                                height=100,
                                border_radius=50,
                                bgcolor=theme.bg_field,
                                alignment=ft.alignment.center,
                            ),
                            ft.Container(height=16),
                            ft.Text("No expenses yet", color=theme.text_secondary, size=18, weight=ft.FontWeight.W_600),
                            ft.Container(height=4),
                            ft.Text("Tap + to add your first expense", color=theme.text_muted, size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        
        page.update()
    
    def show_new_account_form():
        """Show the 'New account' form for manual input."""
        
        # Get current theme
        theme = get_theme()
        
        # Form state
        selected_type = {"value": "Cash"}
        selected_color = {"value": "#3B82F6"}
        
        # Color options
        color_options = [
            "#3B82F6",  # Blue
            "#10B981",  # Green
            "#F59E0B",  # Orange
            "#EF4444",  # Red
            "#8B5CF6",  # Purple
            "#EC4899",  # Pink
            "#06B6D4",  # Cyan
            "#6B7280",  # Gray
        ]
        
        # Account type options
        account_types = ["Cash", "Savings", "Credit Card", "Debit Card", "E-Wallet", "Other"]
        
        def close_form(e):
            page.close(new_account_sheet)
        
        def select_color(color: str):
            selected_color["value"] = color
            # Update color indicators
            for i, ctrl in enumerate(color_row.controls):
                if color_options[i] == color:
                    ctrl.border = ft.border.all(2, "white")
                else:
                    ctrl.border = None
            page.update()
        
        def create_account(e):
            account_name = name_field.value
            if not account_name:
                toast("Please enter account name", "#EF4444")
                return
            
            # Get form values
            account_number = bank_number_field.value or ""
            account_type = type_dropdown.value
            try:
                initial_balance = float(initial_value_field.value or 0)
            except ValueError:
                initial_balance = 0.0
            currency = currency_dropdown.value
            color = selected_color["value"]
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save the new account to database
            db.insert_account(
                user_id=state["user_id"],
                name=account_name,
                account_number=account_number,
                account_type=account_type,
                balance=initial_balance,
                currency=currency,
                color=color,
                created_at=created_at
            )
            
            page.close(new_account_sheet)
            toast(f"Account '{account_name}' created!", "#10B981")
            show_view()  # Refresh the view
        
        # Form fields
        name_field = ft.TextField(
            label="Account name",
            hint_text="e.g., My Wallet, Savings",
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            hint_style=ft.TextStyle(color=theme.text_muted),
            border_radius=12,
            cursor_color=theme.accent_primary,
        )
        
        bank_number_field = ft.TextField(
            label="Bank account number (optional)",
            hint_text="Enter account number",
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            hint_style=ft.TextStyle(color=theme.text_muted),
            border_radius=12,
            cursor_color=theme.accent_primary,
        )
        
        # Type dropdown
        type_dropdown = ft.Dropdown(
            label="Type",
            value="Cash",
            options=[ft.dropdown.Option(t) for t in account_types],
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            border_radius=12,
        )
        
        initial_value_field = ft.TextField(
            label="Initial value",
            hint_text="0.00",
            value="0",
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            hint_style=ft.TextStyle(color=theme.text_muted),
            border_radius=12,
            keyboard_type=ft.KeyboardType.NUMBER,
            prefix_text="₱ ",
            prefix_style=ft.TextStyle(color=theme.text_secondary),
            cursor_color=theme.accent_primary,
        )
        
        # Currency dropdown
        currency_dropdown = ft.Dropdown(
            label="Currency",
            value="PHP",
            options=[
                ft.dropdown.Option("PHP", "₱ Philippine Peso"),
                ft.dropdown.Option("USD", "$ US Dollar"),
                ft.dropdown.Option("EUR", "€ Euro"),
                ft.dropdown.Option("JPY", "¥ Japanese Yen"),
                ft.dropdown.Option("GBP", "£ British Pound"),
            ],
            border_color=theme.border_primary,
            focused_border_color=theme.accent_primary,
            bgcolor=theme.bg_card,
            color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary),
            border_radius=12,
        )
        
        # Color selection row
        color_row = ft.Row(
            controls=[
                ft.Container(
                    width=36,
                    height=36,
                    border_radius=18,
                    bgcolor=color,
                    border=ft.border.all(2, "white") if color == selected_color["value"] else None,
                    on_click=lambda e, c=color: select_color(c),
                    ink=True,
                )
                for color in color_options
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        new_account_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Handle bar
                        ft.Container(
                            content=ft.Container(
                                width=40,
                                height=4,
                                bgcolor=theme.text_muted,
                                border_radius=2,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=12, bottom=16),
                        ),
                        # Header with back button
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=theme.text_secondary,
                                            icon_size=24,
                                            on_click=lambda e: (page.close(new_account_sheet), show_account_type_sheet()),
                                        ),
                                        ft.Text("New account", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                    ],
                                    spacing=8,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=theme.text_secondary,
                                    icon_size=24,
                                    on_click=close_form,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Set up your manual account details",
                            size=14,
                            color=theme.text_muted,
                        ),
                        ft.Container(height=20),
                        # Form fields
                        name_field,
                        ft.Container(height=16),
                        bank_number_field,
                        ft.Container(height=16),
                        type_dropdown,
                        ft.Container(height=16),
                        initial_value_field,
                        ft.Container(height=16),
                        currency_dropdown,
                        ft.Container(height=20),
                        # Color selection
                        ft.Text("Account color", size=14, color=theme.text_secondary),
                        ft.Container(height=12),
                        color_row,
                        ft.Container(height=24),
                        # Create button
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ADD_CIRCLE, color="white", size=20),
                                    ft.Container(width=8),
                                    ft.Text("Create Account", size=16, weight=ft.FontWeight.W_600, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.symmetric(vertical=16),
                            border_radius=12,
                            bgcolor=theme.accent_primary,
                            on_click=create_account,
                            ink=True,
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24),
            ),
            bgcolor=theme.bg_secondary,
        )
        
        page.open(new_account_sheet)
    
    def show_account_settings():
        """Show the Account Settings screen for managing accounts."""
        
        # Get current theme
        theme = get_theme()
        
        def show_edit_account_form(account_data):
            """Show form to edit an existing account."""
            acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color, is_primary, created_at, acc_status, sort_order = account_data
            
            # Form state
            selected_type = {"value": acc_type}
            selected_color = {"value": acc_color}
            selected_status = {"value": acc_status}
            
            # Color options
            color_options = [
                "#3B82F6",  # Blue
                "#10B981",  # Green
                "#F59E0B",  # Orange
                "#EF4444",  # Red
                "#8B5CF6",  # Purple
                "#EC4899",  # Pink
                "#06B6D4",  # Cyan
                "#6B7280",  # Gray
            ]
            
            # Account type options
            account_types = ["Cash", "Savings", "Credit Card", "Debit Card", "E-Wallet", "Other"]
            
            def close_edit(e):
                page.close(edit_sheet)
            
            def select_color(color: str):
                selected_color["value"] = color
                for i, ctrl in enumerate(color_row.controls):
                    if color_options[i] == color:
                        ctrl.border = ft.border.all(2, "white")
                    else:
                        ctrl.border = None
                page.update()
            
            def select_status(status: str):
                selected_status["value"] = status
                # Update status button styles
                for btn in status_row.controls:
                    if hasattr(btn, 'data') and btn.data == status:
                        btn.bgcolor = "#3B82F6"
                        btn.content.controls[1].color = "white"
                    elif hasattr(btn, 'data'):
                        btn.bgcolor = "#1a1a2e"
                        btn.content.controls[1].color = "#9CA3AF"
                page.update()
            
            def save_account(e):
                new_name = name_field.value
                if not new_name:
                    toast("Please enter account name", "#EF4444")
                    return
                
                # Get form values
                new_account_number = bank_number_field.value or ""
                new_type = type_dropdown.value
                try:
                    new_balance = float(balance_field.value or 0)
                except ValueError:
                    new_balance = acc_balance
                new_currency = currency_dropdown.value
                new_color = selected_color["value"]
                new_status = selected_status["value"]
                
                # Update in database
                db.update_account(
                    account_id=acc_id,
                    user_id=state["user_id"],
                    name=new_name,
                    account_number=new_account_number,
                    account_type=new_type,
                    balance=new_balance,
                    currency=new_currency,
                    color=new_color,
                    status=new_status
                )
                
                page.close(edit_sheet)
                settings_sheet.open = False
                page.update()
                toast(f"Account '{new_name}' updated!", "#10B981")
                show_view()  # Refresh
            
            def delete_account_confirm(e):
                # Prevent deleting primary account
                if is_primary == 1:
                    toast("Cannot delete primary Cash account", "#F59E0B")
                    return
                
                def confirm_delete(e):
                    db.delete_account(acc_id, state["user_id"])
                    page.close(confirm_dialog)
                    page.close(edit_sheet)
                    settings_sheet.open = False
                    page.update()
                    toast(f"Account '{acc_name}' deleted", "#EF4444")
                    show_view()
                
                def cancel_delete(e):
                    page.close(confirm_dialog)
                
                confirm_dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Delete Account?", color="white"),
                    content=ft.Text(f"Are you sure you want to delete '{acc_name}'? This action cannot be undone.", color="#9CA3AF"),
                    bgcolor="#1a1a2e",
                    actions=[
                        ft.TextButton("Cancel", on_click=cancel_delete),
                        ft.TextButton("Delete", on_click=confirm_delete, style=ft.ButtonStyle(color="#EF4444")),
                    ],
                )
                page.open(confirm_dialog)
            
            # Form fields
            name_field = ft.TextField(
                label="Account name",
                value=acc_name,
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
                cursor_color=theme.accent_primary,
            )
            
            bank_number_field = ft.TextField(
                label="Bank account number (optional)",
                value=acc_number or "",
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
                cursor_color=theme.accent_primary,
            )
            
            type_dropdown = ft.Dropdown(
                label="Type",
                value=acc_type,
                options=[ft.dropdown.Option(t) for t in account_types],
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
            )
            
            balance_field = ft.TextField(
                label="Balance",
                value=str(acc_balance),
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
                keyboard_type=ft.KeyboardType.NUMBER,
                prefix_text="₱ ",
                prefix_style=ft.TextStyle(color=theme.text_secondary),
                cursor_color=theme.accent_primary,
            )
            
            currency_dropdown = ft.Dropdown(
                label="Currency",
                value=acc_currency,
                options=[
                    ft.dropdown.Option("PHP", "₱ Philippine Peso"),
                    ft.dropdown.Option("USD", "$ US Dollar"),
                    ft.dropdown.Option("EUR", "€ Euro"),
                    ft.dropdown.Option("JPY", "¥ Japanese Yen"),
                    ft.dropdown.Option("GBP", "£ British Pound"),
                ],
                border_color=theme.border_primary,
                focused_border_color=theme.accent_primary,
                bgcolor=theme.bg_card,
                color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary),
                border_radius=12,
            )
            
            # Status selection buttons
            def create_status_btn(label: str, status_value: str, icon):
                is_selected = acc_status == status_value
                return ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon, color="white" if is_selected else theme.text_secondary, size=16),
                            ft.Text(label, size=12, color="white" if is_selected else theme.text_secondary),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=4,
                    ),
                    padding=ft.padding.symmetric(vertical=10, horizontal=12),
                    border_radius=8,
                    bgcolor=theme.accent_primary if is_selected else theme.bg_card,
                    border=ft.border.all(1, theme.accent_primary if is_selected else theme.border_primary),
                    on_click=lambda e, s=status_value: select_status(s),
                    data=status_value,
                    ink=True,
                    expand=True,
                )
            
            status_row = ft.Row(
                controls=[
                    create_status_btn("Active", "active", ft.Icons.CHECK_CIRCLE),
                    create_status_btn("Excluded", "excluded", ft.Icons.REMOVE_CIRCLE_OUTLINE),
                    create_status_btn("Archived", "archived", ft.Icons.ARCHIVE),
                ],
                spacing=8,
            )
            
            # Color selection row
            color_row = ft.Row(
                controls=[
                    ft.Container(
                        width=36,
                        height=36,
                        border_radius=18,
                        bgcolor=color,
                        border=ft.border.all(2, "white") if color == selected_color["value"] else None,
                        on_click=lambda e, c=color: select_color(c),
                        ink=True,
                    )
                    for color in color_options
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            
            edit_sheet = ft.BottomSheet(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            # Handle bar
                            ft.Container(
                                content=ft.Container(
                                    width=40,
                                    height=4,
                                    bgcolor=theme.text_muted,
                                    border_radius=2,
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(top=12, bottom=16),
                            ),
                            # Header
                            ft.Row(
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.Icons.ARROW_BACK,
                                                icon_color=theme.text_secondary,
                                                icon_size=24,
                                                on_click=close_edit,
                                            ),
                                            ft.Text("Edit Account", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                        ],
                                        spacing=8,
                                    ),
                                    # Show Primary badge or Delete button
                                    ft.Container(
                                        content=ft.Row(
                                            controls=[
                                                ft.Icon(ft.Icons.STAR_ROUNDED, size=14, color="#10B981"),
                                                ft.Text("Primary", size=12, color="#10B981", weight=ft.FontWeight.W_600),
                                            ],
                                            spacing=4,
                                        ),
                                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                                        border_radius=12,
                                        bgcolor="#0D3D2E",
                                        visible=is_primary == 1,
                                    ) if is_primary == 1 else ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE,
                                        icon_color=theme.error,
                                        icon_size=24,
                                        on_click=delete_account_confirm,
                                        tooltip="Delete account",
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Container(height=16),
                            # Form fields
                            name_field,
                            ft.Container(height=12),
                            bank_number_field,
                            ft.Container(height=12),
                            type_dropdown,
                            ft.Container(height=12),
                            balance_field,
                            ft.Container(height=12),
                            currency_dropdown,
                            ft.Container(height=16),
                            # Status selection
                            ft.Text("Account Status", size=14, color=theme.text_secondary),
                            ft.Container(height=8),
                            status_row,
                            ft.Container(height=16),
                            # Color selection
                            ft.Text("Account color", size=14, color=theme.text_secondary),
                            ft.Container(height=8),
                            color_row,
                            ft.Container(height=24),
                            # Save button
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.SAVE, color="white", size=20),
                                        ft.Container(width=8),
                                        ft.Text("Save Changes", size=16, weight=ft.FontWeight.W_600, color="white"),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                padding=ft.padding.symmetric(vertical=16),
                                border_radius=12,
                                bgcolor=theme.accent_primary,
                                on_click=save_account,
                                ink=True,
                            ),
                            ft.Container(height=24),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    ),
                    bgcolor=theme.bg_secondary,
                    padding=ft.padding.symmetric(horizontal=20, vertical=0),
                    border_radius=ft.border_radius.only(top_left=24, top_right=24),
                ),
                bgcolor=theme.bg_secondary,
            )
            
            page.open(edit_sheet)
        
        def create_account_settings_card(account_data):
            """Create a card for the account settings list."""
            acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color, is_primary, created_at, acc_status, sort_order = account_data
            
            # Status badge
            status_badges = {
                "active": {"text": "Active", "color": "#10B981", "bg": "#10B98120"},
                "excluded": {"text": "Excluded", "color": "#F59E0B", "bg": "#F59E0B20"},
                "archived": {"text": "Archived", "color": "#6B7280", "bg": "#6B728020"},
            }
            badge_info = status_badges.get(acc_status, status_badges["active"])
            
            # Account type icons
            account_type_icons = {
                "Cash": ft.Icons.ACCOUNT_BALANCE_WALLET,
                "Savings": ft.Icons.SAVINGS,
                "Credit Card": ft.Icons.CREDIT_CARD,
                "Debit Card": ft.Icons.PAYMENT,
                "E-Wallet": ft.Icons.PHONE_ANDROID,
                "Other": ft.Icons.WALLET,
            }
            acc_icon = account_type_icons.get(acc_type, ft.Icons.WALLET)
            
            # Build badges row
            badges = [
                ft.Text(acc_type, size=12, color=theme.text_muted),
            ]
            
            # Add Primary badge if this is the primary account
            if is_primary == 1:
                badges.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.STAR_ROUNDED, size=10, color="#10B981"),
                                ft.Text("Primary", size=10, color="#10B981"),
                            ],
                            spacing=2,
                        ),
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border_radius=4,
                        bgcolor="#0D3D2E",
                    )
                )
            else:
                badges.append(
                    ft.Container(
                        content=ft.Text(badge_info["text"], size=10, color=badge_info["color"]),
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border_radius=4,
                        bgcolor=badge_info["bg"],
                    )
                )
            
            return ft.Container(
                content=ft.Row(
                    controls=[
                        # Drag handle (not for primary)
                        ft.Icon(ft.Icons.DRAG_HANDLE, color=theme.text_muted if is_primary != 1 else "#0D3D2E", size=20),
                        ft.Container(width=8),
                        # Account icon
                        ft.Container(
                            content=ft.Icon(acc_icon, color=acc_color, size=20),
                            width=40,
                            height=40,
                            border_radius=10,
                            bgcolor=f"{acc_color}30",
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(width=12),
                        # Account info
                        ft.Column(
                            controls=[
                                ft.Text(acc_name, size=15, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                ft.Row(
                                    controls=badges,
                                    spacing=8,
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        # Edit icon
                        ft.IconButton(
                            icon=ft.Icons.EDIT_OUTLINED,
                            icon_color=theme.text_muted,
                            icon_size=20,
                            on_click=lambda e, data=account_data: show_edit_account_form(data),
                            tooltip="Edit account",
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=12,
                border_radius=12,
                bgcolor=theme.bg_card,
                border=ft.border.all(1, theme.border_primary),
                on_click=lambda e, data=account_data: show_edit_account_form(data),
                ink=True,
            )
        
        # Get all accounts including archived/excluded
        all_accounts = db.get_accounts_by_user(state["user_id"], include_all=True)
        
        # Build account cards list
        account_settings_cards = []
        for acc in all_accounts:
            account_settings_cards.append(create_account_settings_card(acc))
            account_settings_cards.append(ft.Container(height=8))
        
        # If no accounts, show empty state
        if not all_accounts:
            account_settings_cards.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, color=theme.text_muted, size=48),
                            ft.Container(height=8),
                            ft.Text("No accounts yet", color=theme.text_secondary, size=16),
                            ft.Text("Tap + to add your first account", color=theme.text_muted, size=14),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=40,
                    alignment=ft.alignment.center,
                )
            )
        
        settings_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Handle bar
                        ft.Container(
                            content=ft.Container(
                                width=40,
                                height=4,
                                bgcolor=theme.text_muted,
                                border_radius=2,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=12, bottom=16),
                        ),
                        # Header with back button
                        ft.Row(
                            controls=[
                                ft.Row(
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK,
                                            icon_color=theme.text_secondary,
                                            icon_size=24,
                                            on_click=lambda e: (page.close(settings_sheet), show_view()),
                                        ),
                                        ft.Text("Accounts settings", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                    ],
                                    spacing=8,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=theme.text_secondary,
                                    icon_size=24,
                                    on_click=lambda e: (page.close(settings_sheet), show_view()),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Manage your accounts, change status, or reorder them",
                            size=14,
                            color=theme.text_muted,
                        ),
                        ft.Container(height=16),
                        # Accounts list
                        ft.Column(
                            controls=account_settings_cards,
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
                        ),
                        ft.Container(height=16),
                        # Add Account Button at bottom
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ADD_CIRCLE, color="white", size=20),
                                    ft.Container(width=8),
                                    ft.Text("Add New Account", size=16, weight=ft.FontWeight.W_600, color="white"),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            padding=ft.padding.symmetric(vertical=16),
                            border_radius=12,
                            bgcolor=theme.accent_primary,
                            on_click=lambda e: (page.close(settings_sheet), show_account_type_sheet()),
                            ink=True,
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24),
            ),
            bgcolor=theme.bg_secondary,
        )
        
        page.open(settings_sheet)
    
    def show_account_type_sheet():
        """Show the 'Choose an account type' bottom sheet with account options."""
        
        theme = get_theme()
        
        def close_sheet(e):
            page.close(account_sheet)
        
        def select_account_type(account_type: str):
            page.close(account_sheet)
            if account_type == "Manual Input":
                show_new_account_form()
            else:
                toast(f"{account_type} - Coming soon!", "#3B82F6")
        
        def create_account_type_card(icon, title: str, description: str, on_click):
            """Create an account type option card."""
            return ft.Container(
                content=ft.Row(
                    controls=[
                        # Text content
                        ft.Column(
                            controls=[
                                ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
                                ft.Container(height=4),
                                ft.Text(description, size=12, color=theme.text_muted, max_lines=2),
                            ],
                            spacing=0,
                            expand=True,
                        ),
                        # Icon on right side
                        ft.Container(
                            content=ft.Icon(icon, color="#3B82F6", size=28),
                            width=56,
                            height=56,
                            border_radius=12,
                            bgcolor="#3B82F620",
                            alignment=ft.alignment.center,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=16,
                ),
                padding=16,
                border_radius=12,
                bgcolor=theme.bg_card,
                border=ft.border.all(1, theme.border_primary),
                on_click=on_click,
                ink=True,
            )
        
        account_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Handle bar
                        ft.Container(
                            content=ft.Container(
                                width=40,
                                height=4,
                                bgcolor=theme.text_muted,
                                border_radius=2,
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=12, bottom=16),
                        ),
                        # Header
                        ft.Row(
                            controls=[
                                ft.Text("Choose an account type", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color=theme.text_muted,
                                    icon_size=24,
                                    on_click=close_sheet,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Select how you want to track your finances",
                            size=14,
                            color=theme.text_secondary,
                        ),
                        ft.Container(height=20),
                        # Account type options
                        create_account_type_card(
                            icon=ft.Icons.ACCOUNT_BALANCE,
                            title="Bank Sync",
                            description="Connect your bank for automatic transaction import and real-time balance updates",
                            on_click=lambda e: select_account_type("Bank Sync"),
                        ),
                        ft.Container(height=12),
                        create_account_type_card(
                            icon=ft.Icons.TRENDING_UP,
                            title="Investments",
                            description="Track stocks, crypto, mutual funds and other investment assets",
                            on_click=lambda e: select_account_type("Investments"),
                        ),
                        ft.Container(height=12),
                        create_account_type_card(
                            icon=ft.Icons.UPLOAD_FILE,
                            title="File Import",
                            description="Import transactions from CSV, Excel, or OFX files exported from your bank",
                            on_click=lambda e: select_account_type("File Import"),
                        ),
                        ft.Container(height=12),
                        create_account_type_card(
                            icon=ft.Icons.EDIT_NOTE,
                            title="Manual Input",
                            description="Manually enter and track all your transactions and expenses",
                            on_click=lambda e: select_account_type("Manual Input"),
                        ),
                        ft.Container(height=24),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                bgcolor=theme.bg_secondary,
                padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24),
            ),
            bgcolor=theme.bg_secondary,
        )
        
        page.open(account_sheet)
    
    def show_view():
        page.clean()
        
        # Get current theme
        theme = get_theme()
        
        # Calculate balance
        total_budget = 100000
        total = db.total_expenses_by_user(state["user_id"])
        balance = total_budget - total
        
        # Load expenses
        load_expenses()
        
        # Header with title and profile avatar
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text("Expenses", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                    ft.Container(
                        content=create_user_avatar(state["user_id"], radius=22, theme=theme),
                        on_click=lambda e: show_profile(),
                        ink=True,
                        border_radius=22,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.only(top=10, bottom=16),
        )
        
        # ============ LIST OF ACCOUNT SECTION ============
        # Section header with title and settings icon
        balance_header = ft.Row(
            controls=[
                ft.Text("List of Account", size=20, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                ft.IconButton(
                    icon=ft.Icons.SETTINGS_OUTLINED,
                    icon_color=theme.text_muted,
                    icon_size=22,
                    tooltip="Account Settings",
                    on_click=lambda e: show_account_settings(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        # Get accounts from database
        user_accounts = db.get_accounts_by_user(state["user_id"])
        
        # Icon mapping for account types
        account_type_icons = {
            "Cash": ft.Icons.ACCOUNT_BALANCE_WALLET,
            "Savings": ft.Icons.SAVINGS,
            "Credit Card": ft.Icons.CREDIT_CARD,
            "Debit Card": ft.Icons.PAYMENT,
            "E-Wallet": ft.Icons.PHONE_ANDROID,
            "Other": ft.Icons.WALLET,
        }
        
        # Currency symbols
        currency_symbols = {
            "PHP": "₱",
            "USD": "$",
            "EUR": "€",
            "JPY": "¥",
            "GBP": "£",
        }
        
        def select_account(acc_id, acc_name):
            """Select an account to show in home page balance."""
            state["selected_account_id"] = acc_id
            # Save selection to database for persistence
            db.set_selected_account(state["user_id"], acc_id)
            toast(f"'{acc_name}' selected for balance view", "#10B981")
            # Refresh the view to show selection
            show_view()
        
        # Determine which account is currently selected
        selected_id = state.get("selected_account_id")
        # If no selection in state, load from database
        if selected_id is None:
            selected_account = db.get_selected_account(state["user_id"])
            if selected_account:
                selected_id = selected_account[0]
                state["selected_account_id"] = selected_id
        # If still no selection, default to primary account
        if selected_id is None and user_accounts:
            for acc in user_accounts:
                if acc[7] == 1:  # is_primary
                    selected_id = acc[0]
                    state["selected_account_id"] = selected_id
                    break
        
        # Create account cards list
        account_cards = []
        
        # Create cards for each account from database
        for i, acc in enumerate(user_accounts):
            # acc: (id, name, account_number, type, balance, currency, color, is_primary, created_at)
            acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color, is_primary, created_at = acc
            
            # Get icon and currency symbol
            acc_icon = account_type_icons.get(acc_type, ft.Icons.WALLET)
            curr_symbol = currency_symbols.get(acc_currency, "₱")
            
            # Check if this account is selected
            is_selected = (acc_id == selected_id)
            
            # Determine colors based on primary and selection state
            if is_primary == 1:
                # Primary account - grayed out appearance
                icon_color = "#6B7280"  # Gray
                icon_bg = "#6B728030"
                text_color = theme.text_muted
                border_color = "#10B981" if is_selected else "#6B728050"
            else:
                # Normal account
                icon_color = acc_color
                icon_bg = f"{acc_color}40"
                text_color = theme.text_primary
                border_color = acc_color if is_selected else theme.border_primary
            
            # Build icon column with optional Primary badge
            icon_column_controls = [
                ft.Container(
                    content=ft.Icon(acc_icon, color=icon_color, size=24),
                    width=48,
                    height=48,
                    border_radius=12,
                    bgcolor=icon_bg,
                    alignment=ft.alignment.center,
                ),
            ]
            
            # Add Primary badge below icon for primary account
            if is_primary == 1:
                icon_column_controls.append(
                    ft.Container(
                        content=ft.Text("Primary", size=9, color="#10B981", weight=ft.FontWeight.W_600),
                        padding=ft.padding.symmetric(horizontal=6, vertical=2),
                        border_radius=4,
                        bgcolor="#0D3D2E",
                        margin=ft.margin.only(top=4),
                    )
                )
            
            # Selection indicator (checkmark) - removed, using border only
            
            account_card = ft.Container(
                content=ft.Row(
                    controls=[
                        # Account icon with optional Primary badge
                        ft.Column(
                            controls=icon_column_controls,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=0,
                        ),
                        ft.Container(width=12),
                        # Account info
                        ft.Column(
                            controls=[
                                ft.Text(acc_name, size=16, weight=ft.FontWeight.W_600, color=text_color),
                                ft.Text(
                                    f"{acc_type}" + (f" • {acc_number[-4:]}" if acc_number else ""),
                                    size=12, 
                                    color=theme.text_muted
                                ),
                            ],
                            spacing=2,
                            expand=True,
                        ),
                        # Balance amount
                        ft.Text(
                            f"{curr_symbol}{acc_balance:,.2f}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=text_color if acc_balance >= 0 else theme.error,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=16,
                border_radius=12,
                bgcolor=theme.bg_field,
                border=ft.border.all(2 if is_selected else 1, border_color),
                on_click=lambda e, aid=acc_id, aname=acc_name: select_account(aid, aname),
                ink=True,
            )
            account_cards.append(account_card)
            account_cards.append(ft.Container(height=8))  # Spacing between cards
        
        # Add Account Button - Secondary outline style
        add_account_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color=theme.text_muted, size=20),
                    ft.Container(width=8),
                    ft.Text("Add account", size=14, color=theme.text_muted),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=14),
            border_radius=12,
            border=ft.border.all(1, theme.border_primary),
            bgcolor=theme.bg_field if theme.is_dark else theme.bg_secondary,
            on_click=lambda e: show_account_type_sheet(),
            ink=True,
        )
        
        # Account Detail Button - Blue filled button
        account_detail_btn = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.RECEIPT_LONG, color="white", size=18),
                    ft.Container(width=8),
                    ft.Text("Account Detail", size=14, weight=ft.FontWeight.W_500, color="white"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=12),
            border_radius=10,
            bgcolor="#3B82F6",
            on_click=lambda e: toast("View account details", "#3B82F6"),
            ink=True,
        )
        
        # Balance Card Container - combines all balance elements
        balance_card = ft.Container(
            content=ft.Column(
                controls=[
                    balance_header,
                    ft.Container(height=12),
                    *account_cards,  # Dynamic account cards
                    ft.Container(height=4),
                    add_account_btn,
                    ft.Container(height=12),
                    account_detail_btn,
                ],
            ),
            padding=16,
            border_radius=16,
            bgcolor=theme.bg_card,
            border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
        )
        
        # Main scrollable content
        scrollable_content = ft.Column(
            controls=[
                balance_card,
                ft.Container(height=24),
                expenses_list,
                ft.Container(height=100),  # Space for bottom nav and FAB
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        
        main_content = ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[theme.gradient_start, theme.gradient_end],
            ),
            padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
            content=ft.Column(
                controls=[
                    header,
                    scrollable_content,
                ],
                expand=True,
                spacing=0,
            ),
        )
        
        # Use centralized nav bar component
        full_view = create_page_with_nav(
            page=page,
            main_content=main_content,
            active_index=1,  # Expenses is active
            on_home=show_home,
            on_expenses=None,  # Already on expenses
            on_wallet=show_wallet,
            on_profile=show_profile,
            on_fab_click=show_add_expense,
            theme=theme,
        )
        
        page.add(full_view)
        page.update()
    
    return show_view


# ============ NEW: Content builder for flash-free navigation ============
def build_expenses_content(page: ft.Page, state: dict, toast, 
                            show_home, show_wallet, show_profile, show_add_expense):
    """
    Builds and returns expenses page content WITHOUT calling page.clean() or page.add().
    """
    theme = get_theme()
    
    # Get user profile
    user_profile = db.get_user_profile(state["user_id"])
    first_name = user_profile.get("firstName", "User") if user_profile else "User"
    
    # Create avatar
    user_avatar = create_user_avatar(state["user_id"], radius=22, theme=theme)
    
    # Get accounts
    accounts = db.select_accounts_by_user(state["user_id"])
    selected_account = db.get_selected_account(state["user_id"])
    
    # Get expenses
    expenses = db.select_expenses_by_user(state["user_id"])
    
    # Calculate total balance
    total_balance = sum(acc[4] for acc in accounts) if accounts else 0
    
    # Header
    header = ft.Container(
        content=ft.Row([
            ft.Column([
                ft.Text(f"Hi, {first_name}", size=13, color=theme.text_secondary),
                ft.Text("Expenses", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
            ], spacing=0),
            ft.Row([
                ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE_ROUNDED, icon_color=theme.text_primary, icon_size=22),
                ft.Container(content=user_avatar, on_click=lambda e: show_profile() if show_profile else None,
                            ink=True, border_radius=22),
            ], spacing=8),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(top=10, bottom=16),
    )
    
    # Balance header
    balance_header = ft.Row([
        ft.Column([
            ft.Text("Total Balance", size=12, color=theme.text_secondary),
            ft.Text(f"₱{total_balance:,.2f}", size=28, weight=ft.FontWeight.BOLD, color=theme.text_primary),
        ], spacing=2),
        ft.Icon(ft.Icons.VISIBILITY, color=theme.text_muted, size=20),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    # Account cards
    account_cards = []
    for acc in accounts[:3]:
        acc_id, acc_name, acc_type, is_primary, balance, budget, currency, icon_name, color, is_selected = acc
        
        account_cards.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="white", size=20),
                        width=40, height=40, border_radius=10,
                        bgcolor=color or theme.accent_primary,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text(acc_name, size=14, color=theme.text_primary, weight=ft.FontWeight.W_500),
                        ft.Text(f"₱{balance:,.2f}", size=12, color=theme.text_secondary),
                    ], spacing=2, expand=True),
                    ft.Radio(value=str(acc_id), fill_color=theme.accent_primary) if is_selected else ft.Container(),
                ]),
                padding=12,
                border_radius=12,
                bgcolor=theme.bg_field,
                border=ft.border.all(2 if is_selected else 1, theme.accent_primary if is_selected else theme.border_primary),
            )
        )
        account_cards.append(ft.Container(height=8))
    
    # Balance card
    balance_card = ft.Container(
        content=ft.Column([
            balance_header,
            ft.Container(height=12),
            *account_cards,
        ]),
        padding=16,
        border_radius=16,
        bgcolor=theme.bg_card,
        border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
    )
    
    # Expenses list
    expenses_list = ft.Column(spacing=8)
    
    # Cache account names for efficiency
    account_cache = {}
    def get_account_name(acc_id):
        if acc_id is None:
            return None
        if acc_id not in account_cache:
            acc = db.get_account_by_id(acc_id, state["user_id"])
            account_cache[acc_id] = acc[1] if acc else None
        return account_cache[acc_id]
    
    for exp in expenses[:10]:
        eid, uid, amt, cat, dsc, dtt, acc_id = exp[:7]
        display_name = dsc if dsc else cat
        acc_name = get_account_name(acc_id)
        try:
            dt = datetime.strptime(dtt, "%Y-%m-%d")
            date_str = dt.strftime("%d %b %Y")
        except:
            date_str = dtt
        
        expenses_list.controls.append(
            create_expense_item(
                brand_text=display_name,
                date=date_str,
                amount=-amt,
                theme=theme,
                account_name=acc_name,
            )
        )
    
    if not expenses:
        expenses_list.controls.append(
            ft.Container(
                content=ft.Text("No expenses yet", color=theme.text_secondary, size=14),
                padding=20,
                alignment=ft.alignment.center,
            )
        )
    
    # Scrollable content
    scrollable_content = ft.Column([
        balance_card,
        ft.Container(height=24),
        ft.Text("Recent Transactions", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
        ft.Container(height=12),
        expenses_list,
        ft.Container(height=100),
    ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    main_content = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
        content=ft.Column([header, scrollable_content], expand=True, spacing=0),
    )
    
    return create_page_with_nav(
        page=page,
        main_content=main_content,
        active_index=1,
        on_home=show_home,
        on_expenses=None,
        on_wallet=show_wallet,
        on_profile=show_profile,
        on_fab_click=show_add_expense,
        theme=theme,
    )


# ============ NEW: Content builder for flash-free navigation ============
def build_expenses_content(page: ft.Page, state: dict, toast, 
                           show_home, show_wallet, show_profile, show_add_expense, 
                           show_expenses=None):
    """
    Builds and returns expenses page content WITHOUT calling page.clean() or page.add().
    This reuses the existing view logic but returns content for container swapping.
    """
    # Create a container to hold the content
    content_holder = {"view": None}
    
    # Create the view builder (but don't call show_view yet)
    def capture_view(view):
        content_holder["view"] = view
    
    # We need to build the content directly
    theme = get_theme()
    
    # Get user profile for avatar
    user_profile = db.get_user_profile(state["user_id"])
    first_name = user_profile.get("firstName", "User") if user_profile else "User"
    
    # Create avatar
    user_avatar = create_user_avatar(state["user_id"], radius=22, theme=theme)
    
    # Header
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("My Expenses", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ft.Text("Track your spending", size=13, color=theme.text_secondary),
                    ],
                    spacing=0,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                            icon_color=theme.text_primary,
                            icon_size=22,
                        ),
                        ft.Container(
                            content=user_avatar,
                            on_click=lambda e: show_profile(),
                            ink=True,
                            border_radius=22,
                        ),
                    ],
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.only(top=10, bottom=16),
    )
    
    # Get accounts for balance card
    accounts = db.get_accounts_by_user(state["user_id"])
    selected_account = db.get_selected_account(state["user_id"])
    selected_account_id = selected_account[0] if selected_account else None
    total_balance = sum(acc[4] for acc in accounts) if accounts else 0
    
    # Balance header
    balance_header = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Total Balance", size=12, color=theme.text_secondary),
                    ft.Text(
                        f"₱{total_balance:,.2f}",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=theme.text_primary,
                    ),
                ],
                spacing=4,
            ),
            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color=theme.accent_primary, size=32),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    # Function to select an account
    def select_account(acc_id, acc_name):
        """Select an account to show in home page balance."""
        db.set_selected_account(state["user_id"], acc_id)
        toast(f"'{acc_name}' selected for balance view", "#10B981")
        # Refresh the view by calling show_expenses if available
        if show_expenses:
            show_expenses()
    
    # Build account cards
    account_cards = []
    for acc in (accounts or []):
        # Account structure: id, name, account_number, type, balance, currency, color, is_primary, created_at
        acc_id = acc[0]
        acc_name = acc[1]
        acc_type = acc[3]
        acc_balance = acc[4]
        currency = acc[5]
        color = acc[6]
        is_primary = acc[7]
        is_selected = (acc_id == selected_account_id)
        border_color = theme.accent_primary if is_selected else theme.border_primary
        
        account_card = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.ACCOUNT_BALANCE_WALLET,
                            color=color or theme.accent_primary,
                            size=20,
                        ),
                        bgcolor=f"{color or theme.accent_primary}15",
                        border_radius=10,
                        padding=10,
                    ),
                    ft.Container(width=12),
                    ft.Column(
                        controls=[
                            ft.Text(acc_name, size=14, weight=ft.FontWeight.W_600, color=theme.text_primary),
                            ft.Text(acc_type, size=11, color=theme.text_secondary),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"₱{acc_balance:,.2f}",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=theme.text_primary,
                            ),
                            ft.Text(
                                "Selected" if is_selected else "",
                                size=10,
                                color=theme.accent_primary,
                            ),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=12),
            border_radius=12,
            bgcolor=theme.bg_field,
            border=ft.border.all(2 if is_selected else 1, border_color),
            on_click=lambda e, aid=acc_id, aname=acc_name: select_account(aid, aname),
            ink=True,
        )
        account_cards.append(account_card)
        account_cards.append(ft.Container(height=8))
    
    # ============ Add Account Form ============
    def show_new_account_form(e=None):
        """Show the 'New account' form for manual input."""
        # Form state
        selected_color = {"value": "#3B82F6"}
        color_options = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4", "#6B7280"]
        account_types = ["Cash", "Savings", "Credit Card", "Debit Card", "E-Wallet", "Other"]
        
        def close_form(e):
            page.close(new_account_sheet)
        
        def select_color(color: str):
            selected_color["value"] = color
            for i, ctrl in enumerate(color_row.controls):
                ctrl.border = ft.border.all(2, "white") if color_options[i] == color else None
            page.update()
        
        def create_account(e):
            account_name = name_field.value
            if not account_name:
                toast("Please enter account name", "#EF4444")
                return
            account_number = bank_number_field.value or ""
            account_type = type_dropdown.value
            try:
                initial_balance = float(initial_value_field.value or 0)
            except ValueError:
                initial_balance = 0.0
            currency = currency_dropdown.value
            color = selected_color["value"]
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            db.insert_account(
                user_id=state["user_id"],
                name=account_name,
                account_number=account_number,
                account_type=account_type,
                balance=initial_balance,
                currency=currency,
                color=color,
                created_at=created_at
            )
            page.close(new_account_sheet)
            toast(f"Account '{account_name}' created!", "#10B981")
            # Refresh the view
            show_home()
        
        name_field = ft.TextField(label="Account name", hint_text="e.g., My Wallet", border_color=theme.border_primary,
            focused_border_color=theme.accent_primary, bgcolor=theme.bg_card, color=theme.text_primary,
            label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12)
        bank_number_field = ft.TextField(label="Bank account number (optional)", hint_text="Enter account number",
            border_color=theme.border_primary, focused_border_color=theme.accent_primary, bgcolor=theme.bg_card,
            color=theme.text_primary, label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12)
        type_dropdown = ft.Dropdown(label="Type", value="Cash", options=[ft.dropdown.Option(t) for t in account_types],
            border_color=theme.border_primary, focused_border_color=theme.accent_primary, bgcolor=theme.bg_card,
            color=theme.text_primary, label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12)
        initial_value_field = ft.TextField(label="Initial value", hint_text="0.00", value="0",
            border_color=theme.border_primary, focused_border_color=theme.accent_primary, bgcolor=theme.bg_card,
            color=theme.text_primary, label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12,
            keyboard_type=ft.KeyboardType.NUMBER, prefix_text="₱ ")
        currency_dropdown = ft.Dropdown(label="Currency", value="PHP",
            options=[ft.dropdown.Option("PHP", "₱ PHP"), ft.dropdown.Option("USD", "$ USD"), ft.dropdown.Option("EUR", "€ EUR")],
            border_color=theme.border_primary, focused_border_color=theme.accent_primary, bgcolor=theme.bg_card,
            color=theme.text_primary, label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12)
        color_row = ft.Row(controls=[ft.Container(width=36, height=36, border_radius=18, bgcolor=c,
            border=ft.border.all(2, "white") if c == selected_color["value"] else None,
            on_click=lambda e, c=c: select_color(c), ink=True) for c in color_options],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        new_account_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Container(content=ft.Container(width=40, height=4, bgcolor=theme.text_muted, border_radius=2),
                        alignment=ft.alignment.center, padding=ft.padding.only(top=12, bottom=16)),
                    ft.Row(controls=[ft.Text("New account", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.text_secondary, icon_size=24, on_click=close_form)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    ft.Text("Set up your account details", size=14, color=theme.text_muted),
                    ft.Container(height=20),
                    name_field, ft.Container(height=16), bank_number_field, ft.Container(height=16),
                    type_dropdown, ft.Container(height=16), initial_value_field, ft.Container(height=16),
                    currency_dropdown, ft.Container(height=20),
                    ft.Text("Account color", size=14, color=theme.text_secondary),
                    ft.Container(height=12), color_row, ft.Container(height=24),
                    ft.Container(content=ft.Row(controls=[ft.Icon(ft.Icons.ADD_CIRCLE, color="white", size=20),
                        ft.Container(width=8), ft.Text("Create Account", size=16, weight=ft.FontWeight.W_600, color="white")],
                        alignment=ft.MainAxisAlignment.CENTER),
                        padding=ft.padding.symmetric(vertical=16), border_radius=12, bgcolor=theme.accent_primary,
                        on_click=create_account, ink=True),
                    ft.Container(height=24),
                ], scroll=ft.ScrollMode.AUTO),
                bgcolor=theme.bg_secondary, padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24)),
            bgcolor=theme.bg_secondary)
        page.open(new_account_sheet)
    
    # ============ Show Account Settings (Edit/Delete) ============
    def show_account_settings(e=None):
        """Show account settings to edit or delete accounts."""
        all_accounts = db.get_accounts_by_user(state["user_id"], include_all=True)
        
        def close_settings(e):
            page.close(settings_sheet)
        
        def show_edit_form(acc):
            acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color = acc[:7]
            is_primary = acc[7] if len(acc) > 7 else 0
            
            selected_color = {"value": acc_color or "#3B82F6"}
            color_options = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899", "#06B6D4", "#6B7280"]
            account_types = ["Cash", "Savings", "Credit Card", "Debit Card", "E-Wallet", "Other"]
            
            name_field = ft.TextField(label="Account name", value=acc_name, border_color=theme.border_primary,
                focused_border_color=theme.accent_primary, bgcolor=theme.bg_card, color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12)
            balance_field = ft.TextField(label="Balance", value=str(acc_balance), border_color=theme.border_primary,
                focused_border_color=theme.accent_primary, bgcolor=theme.bg_card, color=theme.text_primary,
                label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12, keyboard_type=ft.KeyboardType.NUMBER, prefix_text="₱ ")
            type_dropdown = ft.Dropdown(label="Type", value=acc_type, options=[ft.dropdown.Option(t) for t in account_types],
                border_color=theme.border_primary, focused_border_color=theme.accent_primary, bgcolor=theme.bg_card,
                color=theme.text_primary, label_style=ft.TextStyle(color=theme.text_secondary), border_radius=12)
            
            def select_color(color):
                selected_color["value"] = color
                for i, ctrl in enumerate(color_row.controls):
                    ctrl.border = ft.border.all(2, "white") if color_options[i] == color else None
                page.update()
            
            color_row = ft.Row(controls=[ft.Container(width=36, height=36, border_radius=18, bgcolor=c,
                border=ft.border.all(2, "white") if c == selected_color["value"] else None,
                on_click=lambda e, c=c: select_color(c), ink=True) for c in color_options],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            
            def save_changes(e):
                new_name = name_field.value
                try:
                    new_balance = float(balance_field.value or 0)
                except ValueError:
                    new_balance = acc_balance
                new_type = type_dropdown.value
                new_color = selected_color["value"]
                
                db.update_account(acc_id, state["user_id"], name=new_name, account_type=new_type, 
                                 balance=new_balance, color=new_color)
                page.close(edit_sheet)
                page.close(settings_sheet)
                toast(f"Account '{new_name}' updated!", "#10B981")
                show_home()
            
            def delete_account(e):
                if is_primary:
                    toast("Cannot delete primary account", "#EF4444")
                    return
                db.delete_account(acc_id, state["user_id"])
                page.close(edit_sheet)
                page.close(settings_sheet)
                toast(f"Account deleted", "#EF4444")
                show_home()
            
            edit_sheet = ft.BottomSheet(
                content=ft.Container(
                    content=ft.Column(controls=[
                        ft.Container(content=ft.Container(width=40, height=4, bgcolor=theme.text_muted, border_radius=2),
                            alignment=ft.alignment.center, padding=ft.padding.only(top=12, bottom=16)),
                        ft.Row(controls=[ft.Text("Edit Account", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                            ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.text_secondary, icon_size=24, 
                                         on_click=lambda e: page.close(edit_sheet))],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Container(height=16),
                        name_field, ft.Container(height=16), balance_field, ft.Container(height=16),
                        type_dropdown, ft.Container(height=20),
                        ft.Text("Account color", size=14, color=theme.text_secondary),
                        ft.Container(height=12), color_row, ft.Container(height=24),
                        ft.Row(controls=[
                            ft.Container(content=ft.Text("Delete", size=14, color="#EF4444"),
                                padding=ft.padding.symmetric(vertical=14, horizontal=24), border_radius=12,
                                border=ft.border.all(1, "#EF4444"), on_click=delete_account, ink=True),
                            ft.Container(content=ft.Text("Save Changes", size=14, color="white", weight=ft.FontWeight.W_600),
                                padding=ft.padding.symmetric(vertical=14, horizontal=24), border_radius=12,
                                bgcolor=theme.accent_primary, on_click=save_changes, ink=True, expand=True),
                        ], spacing=12),
                        ft.Container(height=24),
                    ], scroll=ft.ScrollMode.AUTO),
                    bgcolor=theme.bg_secondary, padding=ft.padding.symmetric(horizontal=20, vertical=0),
                    border_radius=ft.border_radius.only(top_left=24, top_right=24)),
                bgcolor=theme.bg_secondary)
            page.open(edit_sheet)
        
        # Build account cards for settings
        account_cards_list = []
        for acc in (all_accounts or []):
            acc_id, acc_name, acc_number, acc_type, acc_balance, acc_currency, acc_color = acc[:7]
            is_primary = acc[7] if len(acc) > 7 else 0
            
            account_cards_list.append(ft.Container(
                content=ft.Row(controls=[
                    ft.Container(content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color=acc_color or theme.accent_primary, size=20),
                        bgcolor=f"{acc_color or theme.accent_primary}15", border_radius=10, padding=10),
                    ft.Container(width=12),
                    ft.Column(controls=[
                        ft.Row(controls=[ft.Text(acc_name, size=14, weight=ft.FontWeight.W_600, color=theme.text_primary),
                            ft.Container(content=ft.Text("Primary", size=10, color=theme.accent_primary),
                                bgcolor=f"{theme.accent_primary}20", padding=ft.padding.symmetric(horizontal=8, vertical=2),
                                border_radius=4, visible=is_primary == 1)], spacing=8),
                        ft.Text(f"₱{acc_balance:,.2f}", size=12, color=theme.text_secondary),
                    ], spacing=2, expand=True),
                    ft.Icon(ft.Icons.EDIT_OUTLINED, color=theme.text_muted, size=20),
                ]),
                padding=ft.padding.symmetric(horizontal=14, vertical=12), border_radius=12,
                bgcolor=theme.bg_field, border=ft.border.all(1, theme.border_primary),
                on_click=lambda e, a=acc: show_edit_form(a), ink=True))
            account_cards_list.append(ft.Container(height=8))
        
        if not all_accounts:
            account_cards_list.append(ft.Container(
                content=ft.Text("No accounts yet", color=theme.text_muted, size=14),
                padding=20, alignment=ft.alignment.center))
        
        settings_sheet = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(controls=[
                    ft.Container(content=ft.Container(width=40, height=4, bgcolor=theme.text_muted, border_radius=2),
                        alignment=ft.alignment.center, padding=ft.padding.only(top=12, bottom=16)),
                    ft.Row(controls=[ft.Text("Account Settings", size=22, weight=ft.FontWeight.BOLD, color=theme.text_primary),
                        ft.IconButton(icon=ft.Icons.CLOSE, icon_color=theme.text_secondary, icon_size=24, on_click=close_settings)],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Container(height=8),
                    ft.Text("Tap an account to edit", size=14, color=theme.text_muted),
                    ft.Container(height=16),
                    *account_cards_list,
                    ft.Container(height=24),
                ], scroll=ft.ScrollMode.AUTO),
                bgcolor=theme.bg_secondary, padding=ft.padding.symmetric(horizontal=20, vertical=0),
                border_radius=ft.border_radius.only(top_left=24, top_right=24)),
            bgcolor=theme.bg_secondary)
        page.open(settings_sheet)
    
    # Account list section header with settings icon (defined after show_account_settings)
    account_list_header = ft.Row(
        controls=[
            ft.Text("List of Account", size=16, weight=ft.FontWeight.W_600, color=theme.text_primary),
            ft.IconButton(
                icon=ft.Icons.SETTINGS_OUTLINED,
                icon_color=theme.text_muted,
                icon_size=20,
                tooltip="Account Settings",
                on_click=show_account_settings,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
    
    # Add account button
    add_account_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color=theme.text_muted, size=20),
                ft.Container(width=8),
                ft.Text("Add account", size=14, color=theme.text_muted),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=14),
        border_radius=12,
        border=ft.border.all(1, theme.border_primary),
        bgcolor=theme.bg_field if theme.is_dark else theme.bg_secondary,
        on_click=show_new_account_form,
        ink=True,
    )
    
    # Account detail button
    account_detail_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.RECEIPT_LONG, color="white", size=18),
                ft.Container(width=8),
                ft.Text("Account Detail", size=14, weight=ft.FontWeight.W_500, color="white"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(vertical=12),
        border_radius=10,
        bgcolor="#3B82F6",
        ink=True,
    )
    
    # Balance card
    balance_card = ft.Container(
        content=ft.Column(
            controls=[
                balance_header,
                ft.Container(height=16),
                account_list_header,
                ft.Container(height=8),
                *account_cards,
                ft.Container(height=4),
                add_account_btn,
                ft.Container(height=12),
                account_detail_btn,
            ],
        ),
        padding=16,
        border_radius=16,
        bgcolor=theme.bg_card,
        border=ft.border.all(1, theme.border_primary) if not theme.is_dark else None,
    )
    
    # Expenses list
    expenses_list = ft.Column(spacing=4)
    rows = db.select_expenses_by_user(state["user_id"])
    
    # Cache account names for efficiency
    account_cache = {}
    def get_account_name(acc_id):
        if acc_id is None:
            return None
        if acc_id not in account_cache:
            acc = db.get_account_by_id(acc_id, state["user_id"])
            account_cache[acc_id] = acc[1] if acc else None
        return account_cache[acc_id]
    
    def format_date(date_str):
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%d %b %Y")
        except:
            return date_str
    
    for r in rows:
        eid, uid, amt, cat, dsc, dtt, acc_id = r[:7]
        display_name = dsc if dsc else cat
        acc_name = get_account_name(acc_id)
        expenses_list.controls.append(
            create_expense_item(
                brand_text=display_name,
                date=format_date(dtt),
                amount=-amt,
                theme=theme,
                account_name=acc_name,
            )
        )
    
    if not rows:
        expenses_list.controls.append(
            ft.Container(
                content=ft.Text("No expenses yet!", color="#6B7280", size=14),
                padding=20,
                alignment=ft.alignment.center,
            )
        )
    
    # Main scrollable content
    scrollable_content = ft.Column(
        controls=[
            balance_card,
            ft.Container(height=24),
            expenses_list,
            ft.Container(height=100),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    
    main_content = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[theme.gradient_start, theme.gradient_end],
        ),
        padding=ft.padding.only(left=20, right=20, top=10, bottom=0),
        content=ft.Column(
            controls=[header, scrollable_content],
            expand=True,
            spacing=0,
        ),
    )
    
    return create_page_with_nav(
        page=page,
        main_content=main_content,
        active_index=1,
        on_home=show_home,
        on_expenses=None,
        on_wallet=show_wallet,
        on_profile=show_profile,
        on_fab_click=show_add_expense,
        theme=theme,
    )
