from oauth2client.service_account import ServiceAccountCredentials 
import httplib2, json

class Instant_Indexing:
    SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
    # ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    ENDPOINT = "https://indexing.googleapis.com/batch"

    # service_account_file.json is the private key that you created for your service account. 

    JSON_KEY_FILE = 'api-key.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())

    def indexURL(self, url, http = http):
        # print(type(url)); print("URL: {}".format(url));return;

        ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
        
        # con = 0
        # for u in url:
            # print("U: {} type: {}".format(u, type(u)))
        
        content = {}
        content['url'] = url
        content['type'] = "URL_UPDATED"
        json_ctn = json.dumps(content)
        # print(content)
        # exit()
        # print(json_ctn);return

        response_header, content = http.request(ENDPOINT, method="POST", body=json_ctn)
        # print(content);
        result = json.loads(content.decode())
        # print(result);return
        # con += 1
        # For debug purpose only
        if("error" in result):
            print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"], result["error"]["message"]))
        else:
            print("\t{}".format(result["urlNotificationMetadata"]["url"]))
            # print("urlNotificationMetadata.latestUpdate.url: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["url"]))
            print("\ttype: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["type"]))
            print("\tnotifyTime: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))

        # delete the indexing file
        # os.remove(local_file)

# """
# data.csv has 2 columns: URL and date.
# I just need the URL column.
# """
# def start_indexing(site):
#     indexing_path = "ready_for_indexing.csv"
#     if isfile(indexing_path) and getsize(indexing_path) > 0:
#         csv = pd.read_csv(indexing_path)
#         csv[["post_name"]].apply(lambda x: indexURL(x, http, indexing_path))