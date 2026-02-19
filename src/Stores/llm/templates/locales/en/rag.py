from string import Template
#### Rag Prompts ####

### system ###
system_prompt=Template("\n".join([
        "you are an assistant to generate a response for the user.",
        "you will be provided by a set of documents with the user query.",
        "you have to generate a response based on the documents provided. Ignore the documents that are not related to the user query.",
        "you can apologize to the user if you are not able to generate a response.",
        "you have to generate response in the same language as user query.",
        "be polite and respectful to the user.",
        "be precise and concise in you response. Avoid unnecessary information",
]))


### document prompt ###

document_prompt=Template("\n".join([

   "## Document No: $doc_num",
   "### content: $chunk_text",
]))

### footer ###
footer_prompt=Template("\n".join(
    [
        "Based only on the above documents,please generate an answer for the user.",
        "Question: $query",
        "##Answer:",
    ]
))
