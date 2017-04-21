import email
import csv
# import markupbase
# import HTMLParser
# read path to emails from command line
# class MyParser(HTMLParser):
#    def __init__(self, output_list=None):
#        HTMLParser.__init__(self)
#        if output_list is None:
#            self.output_list = []
#        else:
#            self.output_list = output_list
#    def handle_starttag(self, tag, attrs):
#        if tag == 'a':
#            self.output_list.append(dict(attrs).get('href'))


class EMailParser:
    def __init__(self, str):
        self.str = str
        self.hasJS_ = self.hasJS()
        self.hasForm_ = self.hasForm()
        self.isHTML_ = self.isHTML()
        self.uppercaseCountInSubject_ = self.uppercaseCountInSubject()
        self.isSenderReplyToDifferent_ = self.isSenderReplyToDifferent()
        self.isGreetingImpersonal_ = self.isGreetingImpersonal()
        self.uppercaseCountInBody_ = self.uppercaseCountInBody()
        self.partsInMessageBody_ = self.partsInMessageBody()
        self.hasNonMatchingURLs_ = self.hasNonMatchingURLs()
        self.hasNonModalDomain_ = self.hasNonModalDomain()
        self.hasIPBasedURLs_ = self.hasIPBasedURLs()
        self.hasRecentDomains_ = self.hasRecentDomains()
        self.countLinks_ = self.countLinks()
        self.countDotsInDomain_ = self.countDotsInDomain()
        self.hasRedirects_ = self.hasRedirects()


    def hasToken(self, token):
        print(token)
        if self.str.is_multipart():
            for payload in self.str.get_payload():
                if token in payload.get_payload():
                    print("token found here..")
                    return True
        else:
            if token in self.str.get_payload():
                print("token found")
                return True
        return False

    def hasJS(self):
        return self.hasToken("<script")

    def hasForm(self):
        return self.hasToken("<form")

    def isHTML(self):
        return self.hasToken("<html>")

    def uppercaseCountInSubject(self):
        subj = self.str['Subject']
        return sum(1 for c in subj if c.isupper())

    def isSenderReplyToDifferent(self):
        return True

    def isGreetingImpersonal(self):
        return True

    def uppercaseCountInBody(self):
        count = 0
        if self.str.is_multipart():
            for payload in self.str.get_payload():
                count += sum(1 for c in payload.get_payload() if c.isupper())
        else:
            count += sum(1 for c in self.str.get_payload() if c.isupper())
        return count

    def partsInMessageBody(self):
        count = 0
        if self.str.is_multipart():
            for payload in self.str.get_payload():
                count +=1
            return count
        return 1

    def hasNonMatchingURLs(self):
        #urlParser = MyParser()
        #urlParser.feed(self.str.get_payload(0))
        #urlParser.output_list
        return True

    def hasNonModalDomain(self):
        return True

    def hasIPBasedURLs(self):
        return True

    def hasRecentDomains(self):
        return True

    def countLinks(self):
        return 1

    def countDotsInDomain(self):
        return 1

    def hasRedirects(self):
        return True
    def getRow(self):
        return ([self.hasJS_, self.hasForm_, self.isHTML_, self.uppercaseCountInSubject_,
                     self.isSenderReplyToDifferent_, self.isGreetingImpersonal_, self.uppercaseCountInBody_,
                     self.partsInMessageBody_, self.hasNonMatchingURLs_, self.hasNonModalDomain_,
                     self.hasIPBasedURLs_, self.hasRecentDomains_, self.countLinks_, self.countDotsInDomain_,
                     self.hasRedirects_])

# module to append row to csv
def appendToCSVFile(parser, csvFile):
    with open(csvFile, 'w') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        row = parser.getRow()
        wr.writerow(row)


def processEmail():
    path='/Users/satender/Downloads/easy_ham/0946.eb5e7c2de78b6fec81e509923689a7a4'
    csvFile='/Users/satender/Downloads/easy_ham/csvFile'
    msg = email.message_from_file(open(path))
    parser = EMailParser(msg)
    print(msg['Subject'])
    appendToCSVFile(parser, csvFile)

processEmail()