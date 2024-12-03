rows = d1.getUserDownloadDirectory(userName)
        return rows["results"][0]["response"]["result"]["rows"][0][0]["value"]