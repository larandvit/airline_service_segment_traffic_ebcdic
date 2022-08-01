import codecs

# http://www.3480-3590-data-conversion.com/article-mainframe-tape-details.html

file_path_source = r'D:\Projects\Mark Bruyneel\service_segment_data\RG197.SERVSEG.Y70'
file_path_output = r'D:\Projects\Mark Bruyneel\service_segment_data\RG197.SERVSEG.Y70.ebc'

BLOCK_DESCRIPTION_WORD_BYTES = 4

def calc_block_length(block_description_word):
    swap_bytes = block_description_word[-2:] + block_description_word[:2]
    
    return int.from_bytes(swap_bytes, 'big', signed=False)

with codecs.open(file_path_source, "rb") as f_source:
    #read 4 byte Block Description Word (BDW) giving giving the size of the block   
    block_description_word = f_source.read(BLOCK_DESCRIPTION_WORD_BYTES)
    
    if not block_description_word:
        print('Source file is empty')
        
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
        