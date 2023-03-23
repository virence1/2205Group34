@app.route("/endpointDestination",methods=['POST'])
def getData():
        payload = request.get_json()
        #if payload['combo'] =='132D':
                #decrypted_vote=aes_decrypt(payload)
                #response=update_votebank(decrypted_vote)
                #return "Success 200. Vote captured!"+response

        #do the db stuff
        return 'Success'



def aes_decrypt():
        pass
