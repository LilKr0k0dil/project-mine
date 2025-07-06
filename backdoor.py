import os
from config import mcrcon_basic


def add_to_whitelist(nickname):
    os.system(mcrcon_basic + f"\"whitelist add {nickname}\"")
    
def delete_from_whitelist(nickname):
    os.system(mcrcon_basic + f"\"whitelist remove {nickname}\"")
    
def ban(nickname):
    os.system(mcrcon_basic + f"\"ban {nickname}\"")
