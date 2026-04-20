import hashlib
import config
import os


def get_string_md5(input_string,encoding = "utf-8"):
    input_bytes = input_string.encode(encoding = encoding)
    md5_obj = hashlib.md5() 
    md5_obj.update(input_bytes)
    md5_hex = md5_obj.hexdigest()
    return md5_hex

def check_md5(md5_str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path,"w",encoding="utf-8").close()
        return False
    
    else:
        with open(config.md5_path,"r",encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line == md5_str:
                    return True
        
        return False
    
def save_md5(md5_str):
    with open(config.md5_path,"a",encoding="utf-8") as f:
        f.write(md5_str + "\n")

    

