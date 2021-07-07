import re
import emoji

class TextFormat ():
    '''Class that cleans/formats a tweet'''

    def __init__(self):
        pass
    
    def format(self, text):
        '''Clean a tweet'''

        t = self.fEmoji(text)
        t = self.fReplace(t)
        t = self.fTweet(t)
        t = re.sub('[^A-Za-z0-9ñ]+', ' ', t)

        return t

    def fTag(self, text):
        '''Separate tags into words'''

        pascal = re.compile(r'[A-Z]\d*(?:[A-Z\d]*(?=[A-Z]|$)|[a-z])')
        return pascal.sub(lambda m: (' ' if m.start() else '') + m.group().lower(), text)

    def fEmoji(self, text):
        '''Remove emojis from a text string'''

        return emoji.get_emoji_regexp().sub(r'', text)

    def fReplace(self, text):
        '''Replace accented letters in a text string'''

        replacements = (
            ('á', 'a'),
            ('é', 'e'),
            ('í', 'i'),
            ('ó', 'o'),
            ('ú', 'u'),
        )
        
        for a, b in replacements:
            text = text.replace(a, b).replace(a.upper(), b.upper())
            
        return text

    def fTweet(self, text):
        '''Clean up a text string in a tweet'''

        t = re.sub(r'["\']', '', text)
        t = self.fUrl(t)
        t = t.replace('\n', ' ')
        t = t.split(' ')
        
        t_temp = []
        t_cont = False
        for word in t:
            if word == '' or ((word[0] == '@' or word[0] == '#') and t_cont == False):
                continue
            else:
                t_cont = True
            
            if word[0] == '#':
                word = self.fTag(word[1:])

            t_temp.append(word)
        
        t = ' '.join(t_temp)

        return t
    
    def fUrl(self, text):
        '''Remove URLS in a text string'''

        t = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
        
        return t

    def fFormat(self, text, valid):
        '''Remove invalid characters in a text string'''

        t = re.sub(f'[^{valid}]+', ' ', text)

        return t

