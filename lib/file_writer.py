import os

def write_to_file(file_name=None, text=None, text_out_path=None):
    
    with open(os.path.join(text_out_path, file_name), 'w') as fw:
        fw.write(str(text))
    return