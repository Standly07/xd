import os
import asyncio
import subprocess
import threading
import time
import shutil
import requests
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from decoders import NetModDecoder, ZivpnDecoder, XrayPBDecoder, ArmodDecoder, HowdyDecoder, VmessDecoder

# Configuración
TOKEN = os.getenv('BOT_TOKEN', '8009023703:AAG8dRjvVdVSisKsWb1TTU-4OgnA66eNrrA')
bot = AsyncTeleBot(TOKEN, parse_mode='HTML')
start_time = time.time()
BOT_VERSION = "1.0"
OWNER_ID = "7337537905"
OWNER_USERNAME = "fax_Rin"
BETA_MODE = False
GITHUB_TEMPLATE_URL = "https://raw.githubusercontent.com/XTZ404/a/refs/heads/main/template.txt"

# Directorios y archivos JSON
TEMP_DIR = "temp_files"
USERS_FILE = "Plugin/Users.json"
GROUPS_FILE = "Plugin/Group.json"
os.makedirs(TEMP_DIR, exist_ok=True)

def download_file_from_github(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def add_channel_buttons(reply_markup=None):
    if reply_markup is None:
        reply_markup = InlineKeyboardMarkup()
    
    # Verificar si los botones ya existen para no duplicarlos
    has_channel_buttons = False
    if reply_markup.keyboard:
        for row in reply_markup.keyboard:
            for button in row:
                if button.url in ["t.me/nexunteam", "t.me/stnxcp"]:
                    has_channel_buttons = True
                    break
    
    if not has_channel_buttons:
        reply_markup.row(
            InlineKeyboardButton("📢 Canal", url="t.me/nexunteam"),
            InlineKeyboardButton("👥 Grupo", url="t.me/stnxcp")
        )
    
    return reply_markup
    
async def update_bot_code():
    try:
        github_url = "https://raw.githubusercontent.com/Standly07/xd/refs/heads/main/bot.py"
        temp_file = "temp_bot.py"
        
        if download_file_from_github(github_url, temp_file):
            # Verificar que el archivo descargado es válido
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "AsyncTeleBot" in content:  # Verificación básica
                    # Reemplazar el archivo actual
                    shutil.move(temp_file, "bot.py")
                    return True
        return False
    except Exception as e:
        print(f"Error en actualización: {e}")
        return False
        
# Inicializar archivos JSON
for json_file in [USERS_FILE, GROUPS_FILE]:
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            json.dump([], f)

# Extensiones soportadas
BASE_EXTENSIONS = {
    ".mina": ("Scripts/mina.py", ["python3"]),
    ".xscks": ("Scripts/xscks.py", ["python3"]),
    ".hat": ("Scripts/hat.js", ["node"]),
    ".vpnlite": ("Scripts/vpnlite.py", ["python3"]),
    ".xtp": ("Scripts/xtp.py", ["python3"]),
    ".roy": ("Scripts/roy.py", ["python3"]),
    ".sut": ("Scripts/sut.py", ["python3"]),
    ".phc": ("Scripts/phc.py", ["python3"]),
    ".cloudy": ("Scripts/cloudy.py", ["python3"]),
    ".stk": ("Scripts/stk.py", ["python3"]),
    ".rez": ("Scripts/rez.js", ["node"]),
    ".rezl": ("Scripts/rez.js", ["node"]),
    ".sks": ("Scripts/sks.py", ["python3"]),
    ".epro": ("Scripts/ePro.js", ["node"]),
    ".maya": ("Scripts/maya.py", ["python3"]),
    ".aro": ("Scripts/aro.py", ["python3"]),
    ".nm": ("Scripts/netmod.py", ["python3"]),
    ".ipt": ("Scripts/ipt.py", ["python3"]),
    ".ssh": ("Scripts/ssh.py", ["python3"]),
    ".tnl": ("Scripts/tnl.py", ["python3"]),
    ".mrc": ("Scripts/mrc.py", ["python3"]),
    ".dkarl": ("Scripts/dkarl.py", ["python3"]),
    ".mtl": ("Scripts/mtl.py", ["python3"]),
    ".sksrv": ("Scripts/sksrv.py", ["python3"]),
    ".ehil": ("Scripts/ehil.js", ["node"]),
    ".jez": ("Scripts/jez.py", ["python3"]),
    ".sksplus": ("Scripts/sksplus.py", ["python3"]),
    ".json": ("Scripts/hc.py", ["python3"]),
    ".txt": ("Scripts/npv.py", ["python3"]),
    ".jsonsip": ("Scripts/sip.py", ["python3"]),
    ".mij": ("Scripts/mij.py", ["python3"]),
    # Nuevas extensiones agregadas
    ".ost": ("Scripts/ost.py", ["python3"]),
    ".agn": ("Scripts/agn.py", ["python3"]),
    ".vpc": ("Scripts/vpc.py", ["python3"]),
    ".Fɴ": ("Scripts/fn.py", ["python3"]),
    ".cly": ("Scripts/cly.py", ["python3"]),
    ".jvi": ("Scripts/jvi.py", ["python3"]),
    ".jvc": ("Scripts/jvc.py", ["python3"]),
    ".v2i": ("Scripts/v2i.py", ["python3"]),
    ".nxp": ("Scripts/nxp.py", ["python3"]),
    ".sbr": ("Scripts/sbr.py", ["python3"]),
    ".pb": ("Scripts/pb.py", ["python3"]),
    ".tut": ("Scripts/tut.py", ["python3"]),
    ".tmt": ("Scripts/tmt.py", ["python3"]),
    ".temt": ("Scripts/temt.py", ["python3"]),
    ".wcm": ("Scripts/wcm.py", ["python3"]),
    ".tsn": ("Scripts/tsn.py", ["python3"]),
    ".etun": ("Scripts/etun.py", ["python3"]),
    ".pxp": ("Scripts/pxp.py", ["python3"]),
    ".pcx": ("Scripts/pcx.py", ["python3"]),
    ".aipr": ("Scripts/aipr.py", ["python3"]),
    ".ace": ("Scripts/ace.py", ["python3"]),
    ".tsd": ("Scripts/tsd.py", ["python3"]),
    ".aip": ("Scripts/aip.py", ["python3"]),
    ".cbp": ("Scripts/cbp.py", ["python3"]),
    ".cyber": ("Scripts/cyber.py", ["python3"]),
    ".wt": ("Scripts/wt.py", ["python3"]),
    ".fks": ("Scripts/fks.py", ["python3"]),
    ".gv": ("Scripts/gv.py", ["python3"]),
    ".edan": ("Scripts/edan.py", ["python3"]),
    ".pkm": ("Scripts/pkm.py", ["python3"]),
    ".ntr": ("Scripts/ntr.py", ["python3"]),
    ".act": ("Scripts/act.py", ["python3"]),
    ".cnet": ("Scripts/cnet.py", ["python3"]),
    ".gibs": ("Scripts/gibs.py", ["python3"]),
    ".dvd": ("Scripts/dvd.py", ["python3"]),
    ".ezi": ("Scripts/ezi.py", ["python3"]),
    ".ftp": ("Scripts/ftp.py", ["python3"]),
    ".fthp": ("Scripts/fthp.py", ["python3"]),
    ".jph": ("Scripts/jph.py", ["python3"]),
    ".xsks": ("Scripts/xsks.py", ["python3"]),
    ".ht": ("Scripts/ht.py", ["python3"]),
    ".ssi": ("Scripts/ssi.py", ["python3"]),
    ".kt": ("Scripts/kt.py", ["python3"]),
    ".dvs": ("Scripts/dvs.py", ["python3"]),
    ".fnet": ("Scripts/fnet.py", ["python3"]),
    ".mc": ("Scripts/mc.py", ["python3"]),
    ".hub": ("Scripts/hub.py", ["python3"]),
    ".grd": ("Scripts/grd.py", ["python3"]),
    ".hta": ("Scripts/hta.py", ["python3"]),
    ".eug": ("Scripts/eug.py", ["python3"]),
    ".sds": ("Scripts/sds.py", ["python3"]),
    ".htp": ("Scripts/htp.py", ["python3"]),
    ".bbb": ("Scripts/bbb.py", ["python3"]),
    ".ccc": ("Scripts/ccc.py", ["python3"]),
    ".ddd": ("Scripts/ddd.py", ["python3"]),
    ".eee": ("Scripts/eee.py", ["python3"]),
    ".cln": ("Scripts/cln.py", ["python3"]),
    ".cyh": ("Scripts/cyh.py", ["python3"]),
    ".Tcv2": ("Scripts/tcv2.py", ["python3"]),
    ".NT": ("Scripts/nt.py", ["python3"]),
    ".ai": ("Scripts/ai.py", ["python3"]),
    ".cks": ("Scripts/cks.py", ["python3"]),
    ".garuda": ("Scripts/garuda.py", ["python3"]),
    ".tpp": ("Scripts/tpp.py", ["python3"]),
    ".sky": ("Scripts/sky.py", ["python3"]),
    ".skyp": ("Scripts/skyp.py", ["python3"]),
    ".max": ("Scripts/max.py", ["python3"]),
}

BETA_EXTENSIONS = {
    ".hc": ("Scripts/beta_hc.py", ["python3"]),
    ".ehi": ("Scripts/beta_ehi.py", ["python3"]),
    ".npvt": ("Scripts/beta_npvt.py", ["python3"]),
    ".ssc": ("Scripts/beta_ssc.py", ["python3"]),
    ".sip": ("Scripts/beta_sip.py", ["python3"]),
}

# Inicializar decoders
netmod_decoder = NetModDecoder()
zivpn_decoder = ZivpnDecoder()
xraypb_decoder = XrayPBDecoder()
armod_decoder = ArmodDecoder()
howdy_decoder = HowdyDecoder()
vmess_decoder = VmessDecoder()

def load_json(file_name):
    try:
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                json.dump([], f)
            return []
        
        with open(file_name, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def is_admin(user_id):
    users = load_json(USERS_FILE)
    if not isinstance(users, list):
        users = []
    user = next((u for u in users if str(u.get('id')) == str(user_id)), None)
    return user and user.get('rank', 'user').lower() in ['admin', 'owner']

def register_user(user_id, username, first_name):
    users = load_json(USERS_FILE)
    if not isinstance(users, list):
        users = []
    
    user_exists = any(str(user.get('id')) == str(user_id) for user in users)
    
    if not user_exists:
        new_user = {
            "id": user_id,
            "username": username,
            "first_name": first_name,
            "rank": "user",
            "ban": "No",
            "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "premium_expiry": None  # Nuevo campo para la expiración de premium
        }
        users.append(new_user)
        save_json(USERS_FILE, users)
    return users

def save_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def check_premium_expiry():
    users = load_json(USERS_FILE)
    changed = False
    
    for user in users:
        if user.get('rank', '').lower() == 'premium' and user.get('premium_expiry'):
            try:
                expiry_date = datetime.strptime(user['premium_expiry'], "%Y-%m-%d %H:%M:%S")
                if datetime.now() > expiry_date:
                    user['rank'] = 'user'
                    user['premium_expiry'] = None
                    changed = True
            except:
                pass
    
    if changed:
        save_json(USERS_FILE, users)
        
def register_group(group_id, group_title):
    groups = load_json(GROUPS_FILE)
    
    # Verificar si el grupo ya existe (comparando strings)
    if not any(group['id'] == str(group_id) for group in groups):
        new_group = {
            "id": str(group_id),  # Siempre guardar como string
            "title": group_title,
            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        groups.append(new_group)
        save_json(GROUPS_FILE, groups)
        return True
    return False

def is_group_allowed(group_id):
    groups = load_json(GROUPS_FILE)
    return any(str(group['id']) == str(group_id) for group in groups)

def is_owner(user_id):
    users = load_json(USERS_FILE)
    user = next((u for u in users if str(u['id']) == str(user_id)), None)
    return user and user.get('rank', 'user').lower() == 'owner'

def is_premium(user_id):
    check_premium_expiry()  # Verificar expiraciones primero
    users = load_json(USERS_FILE)
    user = next((u for u in users if str(u['id']) == str(user_id)), None)
    
    if not user or user.get('rank', 'user').lower() != 'premium':
        return False
    
    expiry = user.get('premium_expiry')
    if not expiry:
        return True  # Premium sin expiración
    
    try:
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
        return datetime.now() < expiry_date
    except:
        return True  # Si hay error en el formato, asumir que es premium
def is_banned(user_id):
    users = load_json(USERS_FILE)
    user = next((u for u in users if str(u['id']) == str(user_id)), None)
    return user and user.get('ban', 'No') == 'Si'

def ban_user(user_id):
    users = load_json(USERS_FILE)
    for user in users:
        if str(user['id']) == str(user_id):
            user['ban'] = 'Si'
            save_json(USERS_FILE, users)
            return True
    return False

def unban_user(user_id):
    users = load_json(USERS_FILE)
    for user in users:
        if str(user['id']) == str(user_id):
            user['ban'] = 'No'
            save_json(USERS_FILE, users)
            return True
    return False

def update_user_rank(user_id, new_rank):
    users = load_json(USERS_FILE)
    user_found = False
    
    for user in users:
        if str(user['id']) == str(user_id):
            user['rank'] = new_rank
            user_found = True
            break
    
    if not user_found:
        try:
            new_user = {
                "id": user_id,
                "username": "",
                "first_name": "",
                "rank": new_rank,
                "ban": "No",
                "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            users.append(new_user)
            user_found = True
        except:
            pass
    
    if user_found:
        save_json(USERS_FILE, users)
        return True
    return False

def get_active_extensions():
    return {**BASE_EXTENSIONS, **BETA_EXTENSIONS} if BETA_MODE else BASE_EXTENSIONS

def get_uptime():
    seconds = int(time.time() - start_time)
    return str(timedelta(seconds=seconds))

def get_about_message(user):
    beta_status = "🟢 ACTIVO" if BETA_MODE else "🔴 INACTIVO"
    
    users = load_json(USERS_FILE)
    user_data = next((u for u in users if str(u['id']) == str(user.id)), None)
    
    ban_status = "🔴 SI" if user_data and user_data.get('ban') == 'Si' else "🟢 NO"
    rank = user_data.get('rank', 'user').capitalize() if user_data else 'User'
    
    expiry_info = ""
    if user_data and user_data.get('rank', '').lower() == 'premium' and user_data.get('premium_expiry'):
        try:
            expiry_date = datetime.strptime(user_data['premium_expiry'], "%Y-%m-%d %H:%M:%S")
            remaining_days = (expiry_date - datetime.now()).days
            expiry_info = (f"\n├─ Expiración: {expiry_date.strftime('%d-%m-%Y')}"
                          f"\n└─ Días restantes: {remaining_days if remaining_days > 0 else 0}")
        except:
            pass
    
    return (
        f"🤖 <b>DECRYPTOR BOT v{BOT_VERSION}</b>\n\n"
        f"👤 <b>User Info:</b>\n"
        f"├─ ID: <code>{user.id}</code>\n"
        f"├─ Nombre: {user.first_name}\n"
        f"├─ Username: @{user.username if user.username else 'N/A'}\n"
        f"├─ Rango: {rank}{expiry_info}\n"
        f"└─ Ban: {ban_status}\n\n"
        f"🛠️ <b>System Info:</b>\n"
        f"├─ Owner: {OWNER_USERNAME}\n"
        f"├─ Uptime: {get_uptime()}\n"
        f"├─ Modo Beta: {beta_status}\n"
        f"└─ Formatos soportados: {len(get_active_extensions())}\n\n"
        f"🔒 <b>Seguridad:</b>\n"
        "├─ Procesamiento local\n"
        "└─ Auto-limpieza de archivos\n\n"
        "© 2024 VPN Solutions Team"
    )

# Menús y teclados
def create_start_keyboard(user_id):
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("🆘 SOPORTE", callback_data="support"),
        InlineKeyboardButton("ℹ️ INFORMACIÓN", callback_data="about")
    ]
    
    if is_admin(user_id):
        buttons.insert(0, InlineKeyboardButton("👑 ADMIN", callback_data="admin_panel"))
    
    keyboard.row(*buttons)
    return keyboard

def create_support_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("📁 FORMATOS (1/2)", callback_data="support_formats_part1"),
        InlineKeyboardButton("🔗 ESQUEMAS URI", callback_data="support_schemes")
    )
    keyboard.row(
        InlineKeyboardButton("📁 FORMATOS (2/2)", callback_data="support_formats_part2"),
        InlineKeyboardButton("🔧 HERRAMIENTAS", callback_data="support_tools")
    )
    keyboard.row(
        InlineKeyboardButton("🔙 MENÚ PRINCIPAL", callback_data="menu")
    )
    return keyboard

def create_menu_keyboard(user_id):
    keyboard = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("🆘 SOPORTE", callback_data="support"),
        InlineKeyboardButton("ℹ️ INFORMACIÓN", callback_data="about")
    ]
    
    if is_admin(user_id):
        buttons.insert(0, InlineKeyboardButton("👑 ADMIN", callback_data="admin_panel"))
    
    keyboard.row(*buttons)
    return keyboard

def create_admin_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("🔨 Ban User", callback_data="ban_user"),
        InlineKeyboardButton("➕ Add Group", callback_data="add_group")
    )
    keyboard.row(
        InlineKeyboardButton("📋 Lists Groups", callback_data="list_groups"),
        InlineKeyboardButton("➖ Remove Group", callback_data="remove_group")
    )
    keyboard.row(
        InlineKeyboardButton("👤 Change Rank", callback_data="change_rank"),
        InlineKeyboardButton("🚪 Kick Bot", callback_data="kick_bot")
    )
    keyboard.row(
        InlineKeyboardButton("🔄 Reiniciar Bot", callback_data="restart_bot"),
        InlineKeyboardButton("🆕 Update Code", callback_data="update_code")
    )
    beta_button = InlineKeyboardButton("🔧 Beta OFF", callback_data="beta_toggle") if not BETA_MODE else InlineKeyboardButton("🔧 Beta ON", callback_data="beta_toggle")
    keyboard.row(
        beta_button,
        InlineKeyboardButton("🔙 MENÚ", callback_data="menu")
    )
    return keyboard
    
@bot.callback_query_handler(func=lambda call: call.data == "update_code")
async def handle_update_code(call):
    if not is_admin(call.from_user.id):
        await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
        return
    
    await bot.answer_callback_query(call.id, "🔄 Comprobando actualizaciones...")
    
    try:
        # Mostrar mensaje de "Actualizando..."
        msg = await bot.send_message(call.message.chat.id, "🔄 <b>Actualizando código desde GitHub...</b>")
        
        # Ejecutar la actualización
        success = await update_bot_code()
        
        if success:
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=msg.message_id,
                text="✅ <b>Actualización completada</b>\n\nEl bot se reiniciará automáticamente..."
            )
            # Reiniciar después de 2 segundos
            await asyncio.sleep(2)
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=msg.message_id,
                text="❌ <b>Error en la actualización</b>\n\nNo se pudo descargar la versión más reciente o el archivo no es válido."
            )
    except Exception as e:
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=msg.message_id,
            text=f"❌ <b>Error grave durante la actualización</b>\n\n{str(e)}"
        )
        
def create_rank_selection_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("👑 Owner", callback_data="rank_owner"),
        InlineKeyboardButton("🛡️ Admin", callback_data="rank_admin")
    )
    keyboard.row(
        InlineKeyboardButton("⭐ Premium", callback_data="rank_premium"),
        InlineKeyboardButton("🔙 Cancelar", callback_data="admin_panel")
    )
    return keyboard

# Plantillas de soporte
SUPPORT_TEMPLATES = {
    "support_formats_part1": """
🧑‍💻 <b>VPN CONFIGS SUPPORTED (1/2)</b> 🧑‍💻

📌 <b>Formatos Básicos:</b>
├─ HRT PROXY [.HRT]
├─ JEZ PROXY [.JEZ]
├─ SKSPLUS TUNNEL [.sksplus]
├─ HA TUNNEL [.HAT]
├─ EHIL TUNNEL [.EHIL]
├─ SBR Injector [.SBR]
├─ Techoragon Injector [.TVT]
├─ MINA PRO [.MINA]
├─ Ace Injector [.AIP]
├─ JV Custom [.JVC]
├─ Kumul Injector [.KT]
├─ AIO TUNNEL [.XSCKS]
├─ AUSTRO PLUS [.ARO]
├─ Eugine Pro [.eug]
├─ IP TUNNEL [.IPT]
├─ ZIVPN TUNNEL [.ZIV]
├─ OPEN TUNNEL [.TNL]
├─ BINKE TUNNEL [.PCX]
└─ PB INJECTOR [.PB]
""",

    "support_formats_part2": """
🧑‍💻 <b>VPN CONFIGS SUPPORTED (2/2)</b> 🧑‍💻

📌 <b>Formatos Avanzados:</b>
├─ PHC TUNNEL [.PHC]
├─ FN INJECTOR [.FNNETWORK]
├─ JV INJECTOR [.JVI]
├─ MAVENX INJECTOR [.MIJ]
├─ MR CUSTOM [.MRC]
├─ MEGANEKKO [.UWU]
├─ SOCKSREVIVE VOID [.SKSRV.PNG]
├─ HYBRID -243 VPN [.HBD]
├─ REZ TUNNEL [.REZ]
├─ ROYAL TUNNEL+ [.ROY]
├─ SMK TUN+ [.SUT]
├─ SECOND VPN [.VPNLITE]
├─ X TUNNEL PRO [.XTP]
├─ NET MOD [.NM]
├─ David HTTP [.DVD]
├─ Rez Tunnel Lite [.REZL]
├─ STARK VPN [.STK]
├─ SOCKS HTTP [.SKS]
├─ SSH INJECTOR [.SSH]
├─ AGN INJECTOR [.AGN]
├─ OUSS TUNNEL [.OST]
├─ FN INJECTOR [.FN]
├─ BN INJECTOR [.BN]
├─ V2 INJECTOR [.V2I]
├─ CLAY CUSTOM [.CLY]
├─ APK CUSTOM [.ACM]
├─ Ace Injector [.AIP]
├─ E-PROXY [.EPRO]
├─ NexPrime VPN [.nxp]
├─ MAYA TUN UDP [.MAYA]
└─ ACM TUN UDP [.ACM]
""",

    "support_schemes": """
🔗 <b>ESQUEMAS URI SOPORTADOS</b>

🌐 <b>Prefijos válidos:</b>
├─ nm- : NetMod Configs
├─ ar- : ArMod Configs
├─ pb- : XrayPb Configs
└─ zivpn:// : ZIVPN Configs

📝 <b>Ejemplos:</b>
<code>nm-ssh://eyjs</code>
<code>ar-ssh://eyjs</code>
<code>pb-vmess://eyjs</code>
<code>zivpn://eyjabc123==</code>
""",

    "support_tools": """
🛠️ <b>HERRAMIENTAS DISPONIBLES</b>

🔧 <b>Funcionalidades:</b>
├─ Auto-detección de formato
├─ Decodificación en cadena
└─ Procesamiento por lotes

⚡ <b>Comandos:</b>
Coming Soon....
"""
}

# Handlers
@bot.message_handler(commands=['start', 'help', 'menu'])
async def send_welcome(message):
    register_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    
    with open('img/start.jpg', 'rb') as photo:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption="""⚡ <b>¡Bienvenido/a a Axel Decode!</b> ⚡  

Soy un bot especializado en <b>desencriptar archivos</b>, diseñado para asistirte en el proceso de Descifrar datos cifrados.  

<b>Funcionalidades principales: </b>
✔ <b>Desencriptación de archivos</b> (Consulta el botón <b>"Support"</b> para ver las extensiones compatibles).  
✔ Desarrollado en <b>Python</b> para garantizar eficiencia y precisión.  
✔ Interfaz intuitiva y rápida.  

👨💻 <b>Creado por:</b> @fax_Rin""",
            reply_markup=create_start_keyboard(message.from_user.id),
            parse_mode='HTML'
        )

@bot.message_handler(commands=['beta_on'])
async def enable_beta(message):
    global BETA_MODE
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔️ <b>Acceso denegado</b>\n\nSolo el owner (@fax_Rin) puede cambiar el modo Beta.")
        return
    
    if BETA_MODE:
        await bot.reply_to(message, "ℹ️ El modo Beta ya está activado")
    else:
        BETA_MODE = True
        await bot.reply_to(message, "🟢 <b>Modo Beta ACTIVADO</b>\n\nFormatos beta ahora disponibles:\n.hc, .ehi, .npvt, .ssc, .sip")

@bot.message_handler(commands=['beta_off'])
async def disable_beta(message):
    global BETA_MODE
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔️ <b>Acceso denegado</b>\n\nSolo el owner (@fax_Rin) puede cambiar el modo Beta.")
        return
    
    if not BETA_MODE:
        await bot.reply_to(message, "ℹ️ El modo Beta ya está desactivado")
    else:
        BETA_MODE = False
        await bot.reply_to(message, "🔴 <b>Modo Beta DESACTIVADO</b>\n\nFormatos beta ocultos.")

@bot.message_handler(commands=['status'])
async def bot_status(message):
    await bot.reply_to(message, get_about_message(message.from_user))

@bot.message_handler(commands=['ban'])
async def ban_user_cmd(message):
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔ Acceso denegado")
        return
    
    try:
        user_id = int(message.text.split()[1])
        if ban_user(user_id):
            await bot.reply_to(message, f"✅ Usuario {user_id} baneado correctamente")
        else:
            await bot.reply_to(message, f"❌ No se encontró al usuario {user_id}")
    except (IndexError, ValueError):
        await bot.reply_to(message, "❌ Formato incorrecto. Usa: /ban <user_id>")

@bot.message_handler(commands=['unban'])
async def unban_user_cmd(message):
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔ Acceso denegado")
        return
    
    try:
        user_id = int(message.text.split()[1])
        if unban_user(user_id):
            await bot.reply_to(message, f"✅ Usuario {user_id} desbaneado correctamente")
        else:
            await bot.reply_to(message, f"❌ No se encontró al usuario {user_id}")
    except (IndexError, ValueError):
        await bot.reply_to(message, "❌ Formato incorrecto. Usa: /unban <user_id>")

@bot.callback_query_handler(func=lambda call: True)
async def handle_callback(call):
    if call.data == "support":
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "🔍 <b>MENÚ DE SOPORTE</b>\n\nSelecciona una categoría para ver más información:",
            reply_markup=create_support_keyboard()
        )
    elif call.data in SUPPORT_TEMPLATES:
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            SUPPORT_TEMPLATES[call.data],
            reply_markup=create_support_keyboard()
        )
    elif call.data == "about":
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            get_about_message(call.from_user),
            reply_markup=create_menu_keyboard(call.from_user.id)
        )
    elif call.data == "menu":
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "🔓 <b>MENÚ PRINCIPAL</b>\n\nSelecciona una opción:",
            reply_markup=create_start_keyboard(call.from_user.id)
        )
    elif call.data == "admin_panel":
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "👑 <b>PANEL DE ADMINISTRACIÓN</b>\n\nSelecciona una opción:",
            reply_markup=create_admin_keyboard()
        )
    elif call.data == "ban_user":
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "🔨 <b>BANEAR/DESBANEAR USUARIO</b>\n\nEnvía el ID o @username del usuario:\n\n"
            "Ejemplo para banear: <code>/ban 123456</code>\n"
            "Ejemplo para desbanear: <code>/unban 123456</code>",
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton("🔙 ATRÁS", callback_data="admin_panel")
            )
        )
    elif call.data == "add_group":
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "➕ <b>AÑADIR GRUPO</b>\n\nEnvía el ID o enlace del grupo a añadir:",
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton("🔙 ATRÁS", callback_data="admin_panel")
            )
        )
    elif call.data == "list_groups":
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        groups = load_json(GROUPS_FILE)
        if not groups:
            groups_text = "No hay grupos registrados."
        else:
            groups_text = "\n".join([f"📌 {group['title']} (<code>{group['id']}</code>)" for group in groups])
        
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            f"📋 <b>GRUPOS PERMITIDOS</b>\n\n{groups_text}",
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton("🔙 ATRÁS", callback_data="admin_panel")
            )
        )
    elif call.data == "remove_group":
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "➖ <b>REMOVER GRUPO</b>\n\nEnvía el ID del grupo que deseas remover:",
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton("🔙 ATRÁS", callback_data="admin_panel")
            )
        )
    elif call.data == "kick_bot":
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "🚪 <b>EXPULSAR BOT</b>\n\nEnvía el ID del grupo del que quieres que el bot salga:",
            reply_markup=InlineKeyboardMarkup().row(
                InlineKeyboardButton("🔙 ATRÁS", callback_data="admin_panel")
            )
        )
    elif call.data == "restart_bot":
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        await bot.answer_callback_query(call.id, "🔄 Reiniciando bot...", show_alert=True)
        os.execl(sys.executable, sys.executable, *sys.argv)
    elif call.data == "beta_toggle":
        global BETA_MODE
        if not is_admin(call.from_user.id):
            await bot.answer_callback_query(call.id, "⛔ Acceso denegado", show_alert=True)
            return
        
        BETA_MODE = not BETA_MODE
        status = "ACTIVADO" if BETA_MODE else "DESACTIVADO"
        await bot.answer_callback_query(call.id, f"Modo Beta {status}")
        await edit_message(
            call.message.chat.id,
            call.message.message_id,
            "👑 <b>PANEL DE ADMINISTRACIÓN</b>\n\nSelecciona una opción:",
            reply_markup=create_admin_keyboard()
        )

@bot.message_handler(func=lambda message: message.reply_to_message and 
                     message.reply_to_message.text and 
                     "EXPULSAR BOT" in message.reply_to_message.text)
async def process_kick_bot(message):
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔ Acceso denegado")
        return
    
    group_identifier = message.text.strip()
    try:
        group_id = int(group_identifier)
        groups = load_json(GROUPS_FILE)
        groups = [g for g in groups if str(g['id']) != str(group_id)]
        save_json(GROUPS_FILE, groups)
        
        try:
            await bot.leave_chat(group_id)
            await bot.reply_to(message, f"✅ Bot ha salido del grupo {group_id} y ha sido eliminado de la lista de permitidos")
        except Exception as e:
            await bot.reply_to(message, f"⚠️ No se pudo salir del grupo {group_id}, pero fue eliminado de la lista de permitidos. Error: {str(e)}")
            
    except ValueError:
        await bot.reply_to(message, "❌ Formato inválido. Debes enviar solo el ID numérico del grupo")
    except Exception as e:
        await bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(func=lambda message: message.reply_to_message and 
                     message.reply_to_message.text and 
                     "AÑADIR GRUPO" in message.reply_to_message.text)
async def process_add_group(message):
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔ Acceso denegado")
        return
    
    group_identifier = message.text.strip()
    try:
        if group_identifier.lstrip('-').isdigit():
            # Si es un ID numérico
            group_id = int(group_identifier)
            try:
                chat = await bot.get_chat(group_id)
                register_group(str(chat.id), chat.title)  # Asegurarse de convertir a string
                await bot.reply_to(message, f"✅ Grupo añadido: {chat.title} (<code>{chat.id}</code>)")
            except Exception as e:
                await bot.reply_to(message, f"❌ Error al obtener información del grupo: {str(e)}")
        else:
            # Si es un username o enlace
            try:
                chat = await bot.get_chat(group_identifier)
                register_group(str(chat.id), chat.title)  # Asegurarse de convertir a string
                await bot.reply_to(message, f"✅ Grupo añadido: {chat.title} (<code>{chat.id}</code>)")
            except Exception as e:
                await bot.reply_to(message, f"❌ Error al obtener información del grupo: {str(e)}")
    except Exception as e:
        await bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(func=lambda message: message.reply_to_message and 
                     message.reply_to_message.text and 
                     "REMOVER GRUPO" in message.reply_to_message.text)
async def process_remove_group(message):
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔ Acceso denegado")
        return
    
    group_id = message.text.strip()
    groups = load_json(GROUPS_FILE)
    initial_count = len(groups)
    
    groups = [g for g in groups if str(g['id']) != str(group_id)]
    
    if len(groups) < initial_count:
        save_json(GROUPS_FILE, groups)
        await bot.reply_to(message, f"✅ Grupo {group_id} removido correctamente")
    else:
        await bot.reply_to(message, f"❌ No se encontró el grupo {group_id}")

@bot.message_handler(func=lambda message: (
    message.text and 
    any(message.text.startswith(prefix) for prefix in ['nm-', 'ar-', 'pb-', 'howdy://', 'vmess://eyJ', 'zivpn://'])
))
async def handle_special_texts(message):
    if is_banned(message.from_user.id):
        await bot.reply_to(message, "⛔ Tu cuenta ha sido baneada. No puedes usar este bot.")
        return
    
    if not (is_admin(message.from_user.id) or is_premium(message.from_user.id)):
        await bot.reply_to(message, "⛔ Esta función es solo para usuarios premium")
        return
    
    await decode_message(message)

@bot.message_handler(func=lambda message: (
    message.chat.type in ['group', 'supergroup'] and 
    message.content_type == 'document'
))
async def handle_group_documents(message):
    if not is_group_allowed(str(message.chat.id)):
        await bot.reply_to(message, "❌ Group No Permitido")
        return
    
    await handle_document(message)

@bot.message_handler(commands=['rank'])
async def handle_rank_command(message):
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔ Acceso denegado")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 3:
            raise ValueError("Formato incorrecto")
        
        user_id = int(parts[1])
        rank = parts[2].lower()
        
        # Solo días para premium
        days = None
        if rank == 'premium':
            if len(parts) < 4:
                await bot.reply_to(message, "❌ Para premium debes especificar días. Ejemplo: /rank 123456 premium 30")
                return
            try:
                days = int(parts[3])
                if days <= 0:
                    raise ValueError("Días deben ser positivos")
            except ValueError:
                await bot.reply_to(message, "❌ Días debe ser un número positivo")
                return
        
        valid_ranks = ['owner', 'admin', 'premium', 'user']
        if rank not in valid_ranks:
            await bot.reply_to(message, "❌ Rango no válido. Usa: owner, admin, premium o user")
            return
        
        # Solo el owner puede asignar el rango de owner
        if rank == 'owner' and not is_owner(message.from_user.id):
            await bot.reply_to(message, "⛔ Solo el owner puede asignar este rango")
            return
        
        # Calcular fecha de expiración si es premium
        expiry_date = None
        if rank == 'premium' and days is not None:
            expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Actualizar el usuario
        users = load_json(USERS_FILE)
        user_found = False
        
        for user in users:
            if str(user['id']) == str(user_id):
                user['rank'] = rank
                if rank == 'premium':
                    user['premium_expiry'] = expiry_date
                else:
                    user['premium_expiry'] = None
                user_found = True
                break
        
        if not user_found:
            new_user = {
                "id": user_id,
                "username": "",
                "first_name": "",
                "rank": rank,
                "ban": "No",
                "registration_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "premium_expiry": expiry_date if rank == 'premium' else None
            }
            users.append(new_user)
        
        save_json(USERS_FILE, users)
        
        rank_names = {
            'owner': '👑 Owner',
            'admin': '🛡️ Admin',
            'premium': '⭐ Premium',
            'user': '👤 User'
        }
        
        response = f"✅ Rango actualizado correctamente\n\nUsuario: {user_id}\nNuevo rango: {rank_names[rank]}"
        if rank == 'premium':
            response += f"\nExpira: {expiry_date.split()[0]}"
            response += f"\nDías: {days}"
        
        await bot.reply_to(message, response)
        
    except ValueError as e:
        await bot.reply_to(message, f"❌ Formato incorrecto. Usa: /rank ID RANGO [DIAS]\nEjemplo para premium: /rank 123456 premium 30\nEjemplo para user: /rank 123456 user")
    except Exception as e:
        await bot.reply_to(message, f"❌ Error: {str(e)}")

@bot.message_handler(content_types=['document'])
async def handle_document(message):
    if is_banned(message.from_user.id):
        await bot.reply_to(message, "⛔ Tu cuenta ha sido baneada. No puedes usar este bot.")
        return
    
    if not (is_admin(message.from_user.id) or is_premium(message.from_user.id)):
        await bot.reply_to(message, "⛔ Esta función es solo para usuarios premium.")
        return
    
    try:
        file_info = await bot.get_file(message.document.file_id)
        file_ext = os.path.splitext(message.document.file_name)[1].lower()
        
        if file_ext not in get_active_extensions():
            return

        downloaded_file = await bot.download_file(file_info.file_path)
        file_path = os.path.join(TEMP_DIR, message.document.file_name)
        
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        script_name, command = get_active_extensions()[file_ext]
        result = await execute_decrypt_script(script_name, command, file_path)
        
        if result:
            keyboard = InlineKeyboardMarkup()
            keyboard_with_buttons = add_channel_buttons(keyboard)
            await send_long_message(message.chat.id, result, reply_to_message_id=message.message_id)
        
        os.remove(file_path)
            
    except Exception as e:
        keyboard = InlineKeyboardMarkup()
        keyboard_with_buttons = add_channel_buttons(keyboard)
        await bot.reply_to(
            message, 
            f"❌ Error procesando archivo: {str(e)}",
            reply_markup=keyboard_with_buttons
        )
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

async def decode_message(message):
    try:
        text = message.text.strip()
        user = message.from_user
        final_text = None
        
        if text.startswith('nm-'):
            final_text = await netmod_decoder.decode(text, user)
        elif text.startswith('ar-'):
            final_text = await armod_decoder.decode(text, user)
        elif text.startswith('pb-'):
            final_text = await xraypb_decoder.decode(text, user)
        elif text.startswith('zivpn://'):
            final_text = await zivpn_decoder.decode(text, user)
        elif text.startswith('howdy://'):
            final_text = await howdy_decoder.decode(text, user)
        elif text.startswith('vmess://eyJ'):
            final_text = await vmess_decoder.decode(text, user)
        if final_text:
            keyboard = InlineKeyboardMarkup()
            keyboard_with_buttons = add_channel_buttons(keyboard)
            await send_long_message(message.chat.id, final_text, reply_to_message_id=message.message_id)
        else:
            await bot.reply_to(message, "❌ Formato no reconocido o error al decodificar")
            
    except Exception as e:
        error_msg = f"❌ Error procesando mensaje: {str(e)}"
        await send_long_message(message.chat.id, error_msg, reply_to_message_id=message.message_id)

import html

async def send_long_message(chat_id, text, reply_to_message_id=None):
    max_length = 4096
    keyboard = InlineKeyboardMarkup()
    keyboard_with_buttons = add_channel_buttons(keyboard)
    
    # Primero escapamos todo el texto
    escaped_text = html.escape(text)
    
    # Luego restauramos específicamente las etiquetas <code>, </code>, <b> y </b>
    allowed_tags = {
        '&lt;code&gt;': '<code>',
        '&lt;/code&gt;': '</code>',
        '&lt;b&gt;': '<b>',
        '&lt;/b&gt;': '</b>'
    }
    
    # Reemplazamos las versiones escapadas de las etiquetas permitidas
    for escaped_tag, original_tag in allowed_tags.items():
        escaped_text = escaped_text.replace(escaped_tag, original_tag)
    
    for i in range(0, len(escaped_text), max_length):
        part = escaped_text[i:i + max_length]
        await bot.send_message(
            chat_id, 
            part, 
            reply_to_message_id=reply_to_message_id,
            reply_markup=keyboard_with_buttons if i + max_length >= len(escaped_text) else None,
            parse_mode='HTML'
        )

@bot.message_handler(commands=['addgroup'])
async def add_group_command(message):
    if not is_admin(message.from_user.id):
        await bot.reply_to(message, "⛔ Acceso denegado. Solo administradores pueden usar este comando.")
        return
    
    if len(message.text.split()) < 2:
        await bot.reply_to(message, "❌ Uso incorrecto. Por favor usa:\n<code>/addgroup &lt;ID_grupo&gt;</code> o @username", parse_mode='HTML')
        return
    
    group_identifier = message.text.split()[1].strip()
    
    try:
        chat = await bot.get_chat(group_identifier)
        
        if chat.type not in ['group', 'supergroup']:
            await bot.reply_to(message, "❌ El ID proporcionado no pertenece a un grupo válido.")
            return
        
        if register_group(str(chat.id), chat.title):
            response = (
                f"✅ <b>Grupo añadido exitosamente</b>\n\n"
                f"📌 <b>Nombre:</b> {html.escape(chat.title)}\n"
                f"🆔 <b>ID:</b> <code>{chat.id}</code>\n"
                f"👥 <b>Tipo:</b> {chat.type.capitalize()}"
            )
            await bot.reply_to(message, response, parse_mode='HTML')
        else:
            await bot.reply_to(message, "⚠️ Este grupo ya estaba en la lista de permitidos.")
        
    except Exception as e:
        error_message = (
            f"❌ <b>Error al agregar el grupo</b>\n\n"
            f"<code>{html.escape(str(e))}</code>\n\n"
            "Asegúrate de que:\n"
            "1. El bot es miembro del grupo\n"
            "2. El ID o username es correcto\n"
            "3. Usas el formato: <code>/addgroup &lt;ID&gt;</code> o @username"
        )
        await bot.reply_to(message, error_message, parse_mode='HTML')
                                  
async def edit_message(chat_id, message_id, text, reply_markup=None):
    max_retries = 2
    for attempt in range(max_retries):
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
            return True
        except Exception as e:
            if "no text in the message" in str(e) or "message can't be edited" in str(e):
                try:
                    await bot.edit_message_caption(
                        chat_id=chat_id,
                        message_id=message_id,
                        caption=text,
                        reply_markup=reply_markup
                    )
                    return True
                except Exception as caption_error:
                    print(f"Error editing caption: {caption_error}")
                    try:
                        await bot.delete_message(chat_id, message_id)
                        await bot.send_message(
                            chat_id,
                            text,
                            reply_markup=reply_markup,
                            parse_mode='HTML'
                        )
                        return True
                    except Exception as delete_error:
                        print(f"Error in delete-resend strategy: {delete_error}")
                        return False
            elif "message is not modified" in str(e):
                return True
            else:
                print(f"Error editing message (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    try:
                        await bot.send_message(
                            chat_id,
                            text,
                            reply_markup=reply_markup,
                            parse_mode='HTML'
                        )
                        return True
                    except Exception as send_error:
                        print(f"Failed to send new message: {send_error}")
                        return False
                await asyncio.sleep(1)
    return False

async def execute_decrypt_script(script_name, command, file_path):
    script_path = os.path.join(script_name)
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Script no encontrado: {script_path}")
    
    proc = await asyncio.create_subprocess_exec(
        *command, script_path, file_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(
                proc.returncode, command, stdout.decode(), stderr.decode()
            )
        return stdout.decode()
    except asyncio.TimeoutError:
        proc.kill()
        raise Exception("Tiempo de espera excedido")

async def clean_temp_files():
    while True:
        await asyncio.sleep(3600)
        try:
            now = time.time()
            for filename in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, filename)
                if os.path.isfile(file_path):
                    file_age = now - os.path.getmtime(file_path)
                    if file_age > 3600:
                        os.remove(file_path)
                        print(f"🗑️ Archivo temporal eliminado: {filename}")
        except Exception as e:
            print(f"Error en limpieza de archivos: {e}")

async def check_expirations_periodically():
    while True:
        await asyncio.sleep(86400)  # Verificar una vez al día
        check_premium_expiry()

async def main():
    asyncio.create_task(clean_temp_files())
    asyncio.create_task(check_expirations_periodically())
    
    while True:
        try:
            print(f"⚡ Bot v{BOT_VERSION} iniciado - Modo Beta {'ACTIVADO' if BETA_MODE else 'DESACTIVADO'}")
            await bot.polling(non_stop=True, timeout=60)
        except Exception as e:
            print(f"⚠️ Error: {e}. Reconectando en 5s...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
