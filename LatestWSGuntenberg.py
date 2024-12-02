from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import json
import time
import random
import csv

# ------------------------------------------General setup----------------------------------------------------------------
# Information_of_interest=["Author","Date of Birth","Date of Death","Subject","Language","Title"]
Information_of_interest=["Author","Language","Title","Subject","Date of Birth", "Date of Death"]
First_1000_Books=[] #  general storage of book info
books_scanned = 0
for WebIndex in range(1,1000,25):
    url=f"https://www.gutenberg.org/ebooks/search/?sort_order=downloads&start_index={WebIndex}"

    html=urlopen(url).read().decode("utf-8")

    soup=BeautifulSoup(html,"html.parser")

    page_info=[]  #  storage of book info per page 1-25...

    # ------------------------------------------Specific link scraping setup----------------------------------------------------------------

    books_data=soup.find_all("li",class_="booklink")
    for book in books_data:
        book_link = book.a["href"]
        gen_lik="https://www.gutenberg.org"+book_link  # link updater
        print(gen_lik)      # informative purposes

        # ------------------------------------------Specific book scraping setup------------------------------------

        book_dict_info={}   #  storage of book info per table
        list_of_subjects=[]
        url1 = gen_lik

        html1 = urlopen(url1).read().decode("utf-8")

        soup1 = BeautifulSoup(html1, "html.parser")

        # ------------------tables, rows and variables to keep track of the unwanted overwritten keys------------------

        book_table_data=soup1.find("table",class_="bibrec")
        rows=book_table_data.find_all("tr")
        for row in rows : #loops through all the rows of the table data used in the las find.all(tr)

            try:  # takes the headers and the data from each row of the table

                td=row.td.text.strip()
                th=row.th.text.strip()

                print(th+"   "+td)# informative purpose
                print("_----------------------------------------------")# informative purpose

            except: # used to keep scraping when there is no Table header or no Table data, or other exceptions interruptiong the programm
                pass
            if th in Information_of_interest and th == "Subject" and th in book_dict_info:
                book_dict_info["Subject"] += f",{td}"
            elif th in Information_of_interest and th not in book_dict_info:
                print("Should get scraped")
                book_dict_info[th] = td
            if th == "Author"and td.split(",")[-1].strip().split("-")[0].isdigit():
                    book_dict_info["Author"] = f"{td.split()[1]} {td.split()[0]}"
                    book_dict_info["Date of Birth"] = td.split(",")[-1].strip().split("-")[0]
                    book_dict_info["Date of Death"] = td.split(",")[-1].strip().split("-")[1]

            #----------------------------------------------------------------------------------------------------------
            #this section will update our dictbook and check that no keys are overwritten in the specific dictbook information
        try:
            book_dict_info["Subject"]=book_dict_info["Subject"].split(",").strip()
        except:
            pass
                # takes the table headers as keys and the Table data as values and generates the specific book information dictionary
        books_scanned += 1 # informative purpose
        print("_--------------"+ str(books_scanned))# informative purpose
        # ------------------Updating our book info into our page info, and them our page info to our General info of the entire web----------------------------------------------------------------------------------------
        First_1000_Books.append(book_dict_info)

print
#------------------------------------writes to json----------------------------------------------------------------------

# with open("scrapeBook.json","w",encoding="utf-8") as saved_json:
#         json.dump(First_1000_Books,
#                   indent=4,
#                   fp=saved_json,
#                   ensure_ascii=False)
with open("scrapeBook.csv", "w", encoding="utf-8") as saved_csv:
        writer=csv.DictWriter(saved_csv,fieldnames=Information_of_interest)
        writer.writeheader()
        writer.writerows(First_1000_Books)

