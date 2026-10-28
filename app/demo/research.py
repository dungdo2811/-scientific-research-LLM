from langchain_community.document_loaders import DirectoryLoader,UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = DirectoryLoader(
    path= "./papers/", 
    glob="**/*.pdf",
    loader_cls=UnstructuredFileLoader,
    show_progress= True,
    use_multithreading= True
)

docs= loader.load()

print(docs)

MARKDOWN_SEPARATORS = [
    "\n#{1,6} ", ##tách heading
    "```\n",     # tách code block
    "\n\\*\\*\\*+\n",  
    "\n---+\n",      
    "\n___+\n"         
    "\n\n",
    "\n",
    " ",
 *  ""
]

text_splitter= RecursiveCharacterTextSplitter(
    chunk_size= 1200,  ## kích thước của mỗi chunk
    chunk_overlap= 200, ## đoạn chồng lần
    add_start_index= True, ## lưu lại thông tin về vị trí của chunk trong văn bản gốc
    strip_whitespace= True, ## loại bỏ khoảng trắng thừa trong văn bản
    separators= MARKDOWN_SEPARATORS,

)
## ảnh hướng của chunk_size và chunk_overlap đến số lượng chunk 

splits= text_splitter.split_documents(docs)

from pprint import pprint

pprint (splits)




