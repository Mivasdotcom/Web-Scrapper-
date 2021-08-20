from bs4 import BeautifulSoup
import requests
from collections import Counter
import numpy ,pathlib,sys,ast,re,time


class CrawlTool():
    def __init__(self):
        name='CrawlTool'
        #url of the page
        self.url= "http://example.python-scraping.com"


    #function to crwal all links , receive the required information and build the inverted index
    def build(self):

        #all the urls from the website
        all_urls=set()
        #urls that have already been accessed
        visited_urls=set()

        #only urls needed to extract information
        stored_urls=set()

        #array for the tokens of the page
        tokens=[]

        #array of punctuation symbols to be excluded from the inverted index and symbols in general
        punctuations =["<",">","?","(",")","!","," , ";" , "{","}",":","/","-","--","[","]","#" ,"^" ,"@" ,"$","%","&","*","\\d","+","|"]

        #we need only words thus an array of numbers is needed to help us exclude them
        #For the correct creation of the inverted inverted index
        numbers = ['0','1','2','3','4','5','6','7','8','9']

        #dictionaries for inverted index
        inv_dict={}
        new_inv_dict={}

        # getting all the links from the corresponding pages of the website
        pages= numpy.arange(0, 25 , 1)
        for page in pages:
            page=requests.get('http://example.python-scraping.com/places/default/index/'+str(page))

            #initializing our parser
            soup=BeautifulSoup(page.text,'html.parser')

            #extracting the links from each page
            links = soup.find_all('a')

            for link in links:
                #5 second politness window
                time.sleep(5)

                anchor = link.attrs['href']
                #storing all the links into a set
                if anchor.startswith('/'):
                    all_links=self.url+anchor
                    visited_urls.add(all_links)



        #looping through the visited_urls to obtain any more links
        for links1 in visited_urls:
            #5 second politness window
            time.sleep(5)

            response= requests.get(links1)
            soup=BeautifulSoup(response.text,'html.parser')

            more_links=soup.find_all('a')
            for more_links1 in more_links :
                anchor=more_links1.attrs['href']

                if anchor.startswith('/'):
                    all_more_links=self.url+anchor
                    all_urls.add(all_more_links)

                    #filtering the links to obtain only those which provide information
                    #excluding index links to access only the country links and continents

                    if anchor.startswith("/places/default/view/") or anchor.startswith("/places/default/continent/"):
                        local_link=self.url+anchor
                        stored_urls.add(local_link)



        #in case of duplicated links, remove them
        all_links_unique=list()
        for j in all_urls:
            if j not in all_links_unique:
                all_links_unique.append(j)
                #sorting the list asceding order
                list.sort(all_links_unique)
                #enumerating the list
                all_links_unique_enumerated=enumerate(all_links_unique,1)

        #appending the list of all links into a file
        file=pathlib.Path("All_Links_List.txt")
        if file.exists()==False:
            with open("All_Links_List.txt","w") as file_all_links:
                for elements in all_links_unique_enumerated:
                    elements=str(elements)
                    file_all_links.write(elements +'\n')


        #in case of duplicated links, remove them
        result=list()
        for i in stored_urls:
            if i not in result:
                result.append(i)
                #sorting the list ascending order
                list.sort(result)
                #enumarating the links to map the to the corresponding words for the
                #query of the inverted index
                result_enumerated=enumerate(result,1)

        #saving the only the required links into a file
        file=pathlib.Path("Links_List.txt")
        if file.exists()==False:
            with open("Link_List.txt","w") as file_links:
                for elements in result_enumerated:
                    elements=str(elements)
                    file_links.write(elements +'\n')


        #extracing information from each link which was stored in result
        #with the help of the loop we acquired the links once
        for information in result:

            #5 second politness window
            time.sleep(5)

            #receiving the information of the page
            response= requests.get(information)
            soup1=BeautifulSoup(response.text ,'html.parser')


            #receiving the details of the page as text
            text = soup1.get_text(separator='\n',strip=True)

            #Removing punctuations
            for punc in text:
                if punc in punctuations:
                    text= text.replace(punc," ")

            #We only need words thus removing the numbers
            for num in text:
                if num in numbers:
                    text= text.replace(num," ")


            #Splitting the page up /tokenizing
            info=text.split()
            for word in info:
                #remove any words less than 3 letters (including stopwords)
                if len(word) <= 3:
                    info.remove(word)
            tokens.append(info)

        #creating the inverted index
        for i in range(len(tokens)):
            for word in tokens[i]:
                if word not in inv_dict:
                    inv_dict[word]=[]

                if word in inv_dict:
                    inv_dict[word].append(i+1)


        #adding scores for each word
        for score in inv_dict:
            scores=dict(Counter(inv_dict[score]))
            new_inv_dict[score]=[]
            new_inv_dict[score].append(scores)


        #Writing the inverted index into a file
        f=open("inverted_index.txt","w")
        for i in new_inv_dict.keys():
            index= str(new_inv_dict[i]).replace("{","").replace("}", "").replace("'","")
            f.write("{}:{}\n".format(i,index))
        f.close()
        print('Inverted_Index build check your directory')
        return (self.displayWelcome())

    def load(self):
        #loading the inverted index if the inverted_index does not exit
        file=pathlib.Path("inverted_index.txt")
        if file.exists():
            with open('inverted_index.txt',"r") as file:
                lines=file.read()
                return(print(lines))
        else:
            sys.exit("Inverted index file does not exist , (try building the inverted index with build command)")


    def Print(self):
        #using input method to collect the input of the user
        search=input("Enter word to print the corresponding inverted index: ")
        search= search+':'

        file=pathlib.Path("inverted_index.txt")
        if file.exists():
            with open("inverted_index.txt","r") as file:
                for line in file:
                    #setting all the searches as lower
                    #to avoid problems with search
                    line=line.lower()
                    if line.startswith(search):
                        return(print(line))
                else:
                    print('Enter your search word again (in lower) or the word does not exist')
                    return (self.Print())
        else:
            sys.exit("Inverted index file does not exist , (try building the inverted index with build command)")

    def find(self):
        search_choice=input('Enter your phrase: ')
        search_choice=search_choice.split()

        link_list=[]
        lines=[]
        search_result=[]
        result1=[]
        odd=[]
        even=[]
        file=pathlib.Path("inverted_index.txt")
        if file.exists():
            with open("inverted_index.txt","r") as file1:
                for line in file1:
                    line=line.strip()
                    line=line.split(':',1)
                    clean_line=[s.strip('[ ]') for s in line]
                    lines.append(clean_line)
        else:
            sys.exit("Inverted index file does not exist , (try building the inverted index with build command)")

        #receiving the search words
        for i in lines:

            #splitting the list to obtain the position of the word
            if search_choice[0]==i[0]:
                result=search_choice[0] + "," + i[1]
                result=re.split(r"[:,]",result)
                del result[0]
                result1.append(result)

            if len(search_choice)>1:
                if search_choice[1]==i[0]:
                    result=search_choice[1] + ","+ i[1]
                    result=re.split(r"[:,]",result)
                    del result[0]
                    result1.append(result)

        #if no word appended in the list then word does not exist
        if len(result1)==0:

            print('The word/s places do not appear in a link try again')
            return(self.find())


        #receiving the even numbers for link position
        #even numbers for score
        count=0
        for f in range(len(result1)):
            for j in result1[f]:
                if count % 2 == 0:
                    even.append(j)
                if count % 2==1:
                    odd.append(j)
                count +=1


        #receiving the common positions from the given positions of the words
        seen=set()
        dupe=set(x for x in even if x in seen or seen.add(x))

        with open("Link_list.txt","r") as file2:
            for line1 in file2:
                #splitting the list
                line1=line1.split(',')
                #removing any unwanted characters
                clean_number=[s.strip('[]() '' \n') for s in line1]
                link_list.append(clean_number)



        if len(search_choice)==1:
            for f in link_list:
                for k in even:
                    number=str(k).replace(' ','')
                    if number==f[0]:
                        print(f)



        for g in link_list:
            for j in dupe:
                #removing the extra space
                number=str(j).replace(' ','')
                if number==g[0]:
                    print(g)


        return(exit(1))




    def displayWelcome(self):
        print("\n\t\tWelcome To CrawlTool! Please enter your commands")
        print("-------------------------------------------------------------------------------------")
        print("-> Build (use once only once to build the inverted_index)                                ")
        print("-> Load                                                                     ")
        print("-> Print                                                                          ")
        print("-> Find                                                                            ")
        print("-------------------------------------------------------------------------------------")
        while(True):
            command=input("")
            if command=='Build':
                self.build()
            if command=='Load':
                self.load()
                exit(1)
            if command=='Print':
                self.Print()
                exit(1)
            if command=='Find':
                self.find()
            if command=='Exit':
                exit(1)
            else:
                print('Please re-enter your option...(write commands as seen, case sensitive)')
                return(self.displayWelcome())

if __name__ == "__main__":
    c = CrawlTool()
    c.displayWelcome()
