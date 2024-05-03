import xml.etree.cElementTree as ET
import pandas as pd
import datetime
import os
import base64
from pypdf import PdfReader

#Define variables
published = 0 # 0 for not publish, 1 for publish
internal_id = 555 # Maybe set it as year?
volume = 9
number = 1
year = 2023 # YYYY
batch_size = 10

date_published = '2024-04-26' # YYYY-MM-DD
last_modified = '2024-04-26' # YYYY-MM-DD

uploader = 'jpark'
ignore_paper_id = [17, 18, 23] # Should be List


# Set variables
doi = f'10.15353/jcvis.v{volume}i{number}'
issue_title = f'Special Issue: Proceedings of CVIS {year}'
section_id = 7 # We are not sure what this is, but found out that it was consistently 7 in the past publications
current_publication_id = 1
article_id = 10000
submission_id = 20000
file_id = 30000
author_id = 40000
article_galley_id = 50000
starting_page = 1

# Pandas DataFrame with the excel file of the paper meta data
df = pd.read_excel('./Papers.xlsx')

# Get Camera Ready PDF names, paths, and sizes
camera_ready_directory = './CameraReadys 1-37/'
pdf_path = {}
pdf_name = {}
pdf_size = {}
for root, dirs, files in os.walk(camera_ready_directory):
    if len(files) != 0:
        seq_num = root.split('/')[-2]
        file_name = files[0]
        pdf_path[seq_num] = os.path.join(root, files[0])
        pdf_name[seq_num] = files[0]
        pdf_size[seq_num] = os.stat(os.path.join(root, files[0])).st_size


# Begin Creating XML Tree

root = ET.Element("issue")
root.set( "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
root.set("xmlns", "http://pkp.sfu.ca")
root.set("published", f"{published}")
root.set("current", "1")
root.set("access_status", "1")
root.set("url_path", "")
root.set("xsi:schemaLocation", "http://pkp.sfu.ca native.xsd")


ET.SubElement(root, "id", attrib={'type': 'internal', 'advice':'ignore'}).text = str(internal_id)
ET.SubElement(root, "id", attrib={'type': 'doi', 'advice': 'update'}).text = doi

issue_identification = ET.SubElement(root, "issue_identification")
ET.SubElement(issue_identification, "volume").text = str(volume)
ET.SubElement(issue_identification, "number").text = str(number)
ET.SubElement(issue_identification, "year").text = str(year)
ET.SubElement(issue_identification, "title", attrib={'locale': 'en_US'}).text = issue_title

ET.SubElement(root, "date_published").text = date_published
ET.SubElement(root, "last_modified").text = last_modified

sections = ET.SubElement(root, "sections")

section = ET.SubElement(sections, "section", attrib={'ref': 'ART', 'seq': '1', 'editor_restricted': '0',
                                            'meta_indexed': '1', 'meta_reviewed': '1',
                                              'abstracts_not_required': '0', 'hide_title':'0',
                                                'hide_author': '0', 'abstract_word_count': '0'})

ET.SubElement(section, "id", attrib={'type': 'internal', 'advice': 'ignore'}).text = str(section_id)
ET.SubElement(section, "abbrev", attrib={'locale': 'en_US'}).text = 'ART'
ET.SubElement(section, "title", attrib={'locale': 'en_US'}).text = 'Articles'

ET.SubElement(root, 'issue_galleys', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                             "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})

articles = ET.SubElement(root, 'articles', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                             "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})




batch_ind = 0 
batch_count = 0
for index, row in df.iterrows():
    print(row['Paper ID'])
    if int(row['Paper ID']) in ignore_paper_id or not str(row['Paper ID']) in pdf_name:
        continue
    
    date_submitted = row["Last Modified"].split(' ')[0]
    

    date_fixed = datetime.datetime.strptime(date_submitted, "%m/%d/%Y").strftime("%Y-%m-%d")
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    
    article = ET.SubElement(articles, 'article', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                                         'locale':'en_US', 'date_submitted': today,
                                                         'status':'3', "submission_progress":"0",
                                                          "current_publication_id": str(current_publication_id),  "stage":"production"})
    ET.SubElement(article, 'id', attrib={'type':'internal', 'advice':'ignore'}).text = str(article_id)
    
    submission_file = ET.SubElement(article, 'submission_file', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                                                        "id": str(submission_id), 'created_at': today,
                                                                        'date_created': "", 'file_id': str(file_id),
                                                                        'stage': 'submission', 'updated_at':  today,
                                                                        'viewable': 'true', 'genre': 'Article Text',
                                                                        'uploader': uploader, "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})
    

    ET.SubElement(submission_file, 'name', attrib={'locale': 'en_US'}).text = pdf_name[str(row['Paper ID'])]
    file = ET.SubElement(submission_file, 'file', attrib={'id': str(file_id), 'filesize': str(pdf_size[str(row['Paper ID'])]),
                                                'extension': 'pdf'})


    reader = PdfReader(pdf_path[str(row['Paper ID'])])
    pages = len(reader.pages)
    
    with open(pdf_path[str(row['Paper ID'])], "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
    ET.SubElement(file, 'embed', attrib={'encoding': "base64"}).text = encoded_string.decode('ascii')

    
    
    authors_df = row['Author Names'].split(';')
    for idx, temp_authors in enumerate(authors_df):
        if "*" in temp_authors:
            primary_contact_id_offset = idx
            break

    
    
    
    publication = ET.SubElement(article, 'publication', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                                                'locale': 'en_US', 'version': '1', 'status': '3',
                                                                 'primary_contact_id': str(author_id + primary_contact_id_offset),
                                                                  'url_path': "", 'seq': str(row['Paper ID']), 
                                                                   'date_published': today, 'section_ref': 'ART', 'access_status': '0',
                                                                     "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})
    
    ET.SubElement(publication, 'id', attrib={'type': 'internal',
                                             'advice': 'ignore'}).text = str(current_publication_id)
    ET.SubElement(publication, 'id', attrib={'type': 'doi',
                                             'advice': 'update'}).text = doi+'.'+str(article_id)
    ET.SubElement(publication, 'title', attrib={'locale': 'en_US'}).text = row['Paper Title']
    print(row['Paper Title'])
    ET.SubElement(publication, 'abstract', attrib={'locale': 'en_US'}).text = row['Abstract']
    ET.SubElement(publication, 'copyrightHolder', attrib={'locale': 'en_US'}).text = row['Author Names'].split(';')[0].strip().replace('*', '')
    ET.SubElement(publication, 'copyrightYear').text = str(year)

    authors = ET.SubElement(publication, 'authors', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                                            "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})
    
    for author, email in zip(row['Author Names'].split(';'), row['Author Emails'].split(';')):
        author_log = ET.SubElement(authors, 'author', attrib={'include_in_browse': 'true', 'user_group_ref': 'Author',
                                                              'seq': str(row['Paper ID']), 'id': str(author_id)})
        ET.SubElement(author_log, 'givenname', attrib={'locale': 'en_US'}).text = author.split(',')[1].strip().replace('*', '')
        ET.SubElement(author_log, 'familyname', attrib={'locale': 'en_US'}).text = author.split(',')[0].strip().replace('*', '')
        ET.SubElement(author_log, 'country').text = 'CA'
        ET.SubElement(author_log, 'email').text = str(email).strip().replace('*', '')
        author_id += 1

    article_galley = ET.SubElement(publication, 'article_galley', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                                                           'locale': 'en_US', 'url_path': "", 'approved': 'false',
                                                                            "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd" })
    ET.SubElement(article_galley, 'id', attrib={'type': 'internal', 'advice': 'ignore'}).text = str(article_galley_id)
    ET.SubElement(article_galley, 'name', attrib={'locale': 'en_US'}).text = 'PDF'
    ET.SubElement(article_galley, 'seq').text = str(0)
    ET.SubElement(article_galley, 'submission_file_ref', attrib={'id': str(submission_id)})

    ET.SubElement(publication, 'pages').text = f'{starting_page}-{starting_page+pages-1}'                                             


    current_publication_id +=1 
    article_id += 1
    submission_id += 1
    file_id += 1
    article_galley_id +=1 
    
    starting_page += pages

    batch_ind += 1

    if batch_ind == batch_size:
        tree = ET.ElementTree(root)
        ET.indent(tree, '  ')
        tree.write(f"./{batch_count}.xml", xml_declaration=True, encoding='UTF-8')
        batch_count += 1
        batch_ind = 0

        root = ET.Element("issue")
        root.set( "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xmlns", "http://pkp.sfu.ca")
        root.set("published", f"{published}")
        root.set("current", "1")
        root.set("access_status", "1")
        root.set("url_path", "")
        root.set("xsi:schemaLocation", "http://pkp.sfu.ca native.xsd")


        ET.SubElement(root, "id", attrib={'type': 'internal', 'advice':'ignore'}).text = str(internal_id)
        ET.SubElement(root, "id", attrib={'type': 'doi', 'advice': 'update'}).text = doi

        issue_identification = ET.SubElement(root, "issue_identification")
        ET.SubElement(issue_identification, "volume").text = str(volume)
        ET.SubElement(issue_identification, "number").text = str(number)
        ET.SubElement(issue_identification, "year").text = str(year)
        ET.SubElement(issue_identification, "title", attrib={'locale': 'en_US'}).text = issue_title

        ET.SubElement(root, "date_published").text = date_published
        ET.SubElement(root, "last_modified").text = last_modified

        sections = ET.SubElement(root, "sections")

        section = ET.SubElement(sections, "section", attrib={'ref': 'ART', 'seq': '1', 'editor_restricted': '0',
                                                    'meta_indexed': '1', 'meta_reviewed': '1',
                                                    'abstracts_not_required': '0', 'hide_title':'0',
                                                        'hide_author': '0', 'abstract_word_count': '0'})

        ET.SubElement(section, "id", attrib={'type': 'internal', 'advice': 'ignore'}).text = str(section_id)
        ET.SubElement(section, "abbrev", attrib={'locale': 'en_US'}).text = 'ART'
        ET.SubElement(section, "title", attrib={'locale': 'en_US'}).text = 'Articles'

        ET.SubElement(root, 'issue_galleys', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                                    "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})

        articles = ET.SubElement(root, 'articles', attrib={"xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance",
                                                    "xsi:schemaLocation":"http://pkp.sfu.ca native.xsd"})

if batch_ind != 0:
    tree = ET.ElementTree(root)
    ET.indent(tree, '  ')
    tree.write(f"./{batch_count}.xml", xml_declaration=True, encoding='UTF-8')