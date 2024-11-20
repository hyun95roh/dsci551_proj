from mysql import mysqlDB  


def retriever(response):
    retriever = mysqlDB() 
    retriever.disconnect()
    retriever.connect()
    user_input = input("Do you want to see the retreival result? (y, n)")
    if user_input.lower() in ['y','yes']:
        return retriever.execute(response)
    else: 
        return 


