import codecs
import argparse
from os import path
import traceback
import sys

BLOCK_DESCRIPTION_WORD_BYTES = 4

__author__ = "Vitaly Saversky"
__date__ = "2022-07-01"
__credits__ = ["Vitaly Saversky"]
__version__ = "1.0.0"
__maintainer__ = "Vitaly Saversky"
__email__ = "larandvit@hotmail.com"
__status__ = "Production"

def calc_block_length(block_description_word):
    swap_bytes = block_description_word[-2:] + block_description_word[:2]
    
    return int.from_bytes(swap_bytes, 'big', signed=False)

def app_full_name():
    return 'Remove Block Descriptor Word (BDW) bytes from EBCDIC coded files. v.' + __version__

def main():
    
    appArgs = argparse.ArgumentParser()
        
    appArgs.add_argument("--sourcefile", required=True, help="Input file path", metavar='"source file"')
    appArgs.add_argument("--outputfile", required=True, help="Output file path", metavar='"output file"')

    args = appArgs.parse_args()
    
    file_path_source = args.sourcefile
    file_path_output = args.outputfile
    
    if not path.exists(file_path_source):
        print('Source file is not found')
        sys.exit(1)
    
    with codecs.open(file_path_source, "rb") as f_source:
        #read 4 byte Block Description Word (BDW) giving giving the size of the block   
        block_description_word = f_source.read(BLOCK_DESCRIPTION_WORD_BYTES)
        
        if not block_description_word:
            print('Source file is empty')
            sys.exit(1)
            
        else:
            
            block_length = calc_block_length(block_description_word)
            record_length = block_length - BLOCK_DESCRIPTION_WORD_BYTES
            
            record = f_source.read(record_length)
            
            with codecs.open(file_path_output, "wb") as f_output:
            
                while record:
                    
                    f_output.write(record)
                    
                    block_description_word = f_source.read(BLOCK_DESCRIPTION_WORD_BYTES)
                    
                    if block_description_word:
                        block_length = calc_block_length(block_description_word)
                        record_length = block_length - BLOCK_DESCRIPTION_WORD_BYTES
                        
                        record = f_source.read(record_length)
                        
                    else:
                        break
        
if __name__=="__main__":
    try:
        print(app_full_name())
        print()
        main()
        print('File processing has been completed successfully.')
        sys.exit(0)
    except SystemExit:
        #just used to catch system exit exception initiated by sys.exit()
        pass
    except:
        traceback.print_exc()
        sys.exit(1)