import requests, asyncio, json, time, logging

async def req(api_url):
    print("\nFetching API response...")
    res= requests.get(
        url=api_url,
        
    )
    return res

async def main():
    try:
        logger=logging.getLogger(__name__)
        log_formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
        logger.setLevel(logging.DEBUG)
        LOG_FILE_HANDLER=logging.FileHandler(".log")
        LOG_FILE_HANDLER.setLevel(logging.DEBUG)
        LOG_FILE_HANDLER.setFormatter(log_formatter)
        logger.addHandler(LOG_FILE_HANDLER)

        URL=input("Enter gemini API URL: ").strip()

        strt=time.time()
        logger.log(level=20,msg=URL)
        logger.log(level=20,msg="Request processing.")

        respons=await req(URL)

        req_time=time.time()-strt
        status=respons.status_code
        logger.log(level=20,msg=f"Request processed, in {req_time:.2f} seconds. Response status code: {status}")

        if status==200:
            print("Response Fetched successfully.")
        else:
            raise Exception("Invalid URL! Check the URL or the '.log' file for other errors.")

        parsed_res=requests.Response.json(respons)
        records=len(parsed_res['Results'])

        logger.log(level=20,msg=f"Number of records in the response: {records}")

        extracted=set()
        for r in parsed_res['Results']:
            extracted.add(r["Country"])
        print("Extracted data (unique countries):", extracted)

        with open("raw.json", "w", encoding="utf-8") as file:
            json.dump(parsed_res, file, indent=4)
        with open("processed.json", "w", encoding="utf-8") as file:
            json.dump(list(extracted), file, indent=4)

    except requests.HTTPError as e:
        print("\nERROR:",e)
    except Exception as e:
        print("\nERROR:",e)

if __name__=="__main__":
    asyncio.run(main())