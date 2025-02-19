from typing import Optional

class StrCase:
    """
    Helper pour la manipulation des chaînes de caractères.
    
    Example:
        # Snake case -> Camel case
        StrCase.camel('user_name')  # 'userName'
        
        # Camel case -> Snake case
        StrCase.snake('firstName')  # 'first_name'
        
        # Pascal case
        StrCase.pascal('user_name')  # 'UserName'
        
        # Kebab case
        StrCase.kebab('firstName')  # 'first-name'
        
        # Title case
        StrCase.title('user_name')  # 'User Name'
    """
    
    @staticmethod
    def camel(value: str) -> str:
        """
        Convertit une chaîne en camelCase.
        
        Example:
            StrCase.camel('user_name')  # 'userName'
            StrCase.camel('User Name')  # 'userName'
        """
        words = StrCase._split_into_words(value)
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        
    @staticmethod
    def snake(value: str) -> str:
        """
        Convertit une chaîne en snake_case.
        
        Example:
            StrCase.snake('userName')  # 'user_name'
            StrCase.snake('User Name')  # 'user_name'
        """
        words = StrCase._split_into_words(value)
        return '_'.join(word.lower() for word in words)
        
    @staticmethod
    def pascal(value: str) -> str:
        """
        Convertit une chaîne en PascalCase.
        
        Example:
            StrCase.pascal('user_name')  # 'UserName'
            StrCase.pascal('userName')  # 'UserName'
        """
        words = StrCase._split_into_words(value)
        return ''.join(word.capitalize() for word in words)
        
    @staticmethod
    def kebab(value: str) -> str:
        """
        Convertit une chaîne en kebab-case.
        
        Example:
            StrCase.kebab('userName')  # 'user-name'
            StrCase.kebab('User Name')  # 'user-name'
        """
        words = StrCase._split_into_words(value)
        return '-'.join(word.lower() for word in words)
        
    @staticmethod
    def title(value: str) -> str:
        """
        Convertit une chaîne en Title Case.
        
        Example:
            StrCase.title('user_name')  # 'User Name'
            StrCase.title('userName')  # 'User Name'
        """
        words = StrCase._split_into_words(value)
        return ' '.join(word.capitalize() for word in words)
        
    @staticmethod
    def plural(value: str) -> str:
        """
        Retourne le pluriel d'un mot (basique).
        
        Example:
            StrCase.plural('post')  # 'posts'
            StrCase.plural('category')  # 'categories'
        """
        if value.endswith('y'):
            return value[:-1] + 'ies'
        if value.endswith(('s', 'sh', 'ch', 'x', 'z')):
            return value + 'es'
        return value + 's'
        
    @staticmethod
    def singular(value: str) -> str:
        """
        Retourne le singulier d'un mot (basique).
        
        Example:
            StrCase.singular('posts')  # 'post'
            StrCase.singular('categories')  # 'category'
        """
        if value.endswith('ies'):
            return value[:-3] + 'y'
        if value.endswith('es'):
            return value[:-2]
        if value.endswith('s'):
            return value[:-1]
        return value
        
    @staticmethod
    def _split_into_words(value: str) -> list:
        """Divise une chaîne en mots selon différents séparateurs"""
        # Gère les cas avec underscores ou tirets
        if '_' in value:
            return value.split('_')
        if '-' in value:
            return value.split('-')
            
        # Gère le camelCase et PascalCase
        words = []
        current_word = ''
        
        for char in value:
            if char.isupper() and current_word:
                words.append(current_word)
                current_word = char
            else:
                current_word += char
                
        words.append(current_word)
        return words
    
    @staticmethod
    def slug(value: str, separator: str = '-') -> str:
        """
        Crée un slug à partir d'une chaîne.
        
        Example:
            StrCase.slug('Hello World!')  # 'hello-world'
            StrCase.slug('Hello World!', '_')  # 'hello_world'
        """
        import re
        value = value.lower().strip()
        value = re.sub(r'[^\w\s-]', '', value)
        value = re.sub(r'[-\s]+', separator, value)
        return value.strip(separator)
    
    @staticmethod
    def studly(value: str) -> str:
        """
        Convertit une chaîne en StudlyCase (comme PascalCase mais préserve les majuscules).
        
        Example:
            StrCase.studly('hello_world')  # 'HelloWorld'
            StrCase.studly('hello-world')  # 'HelloWorld'
            StrCase.studly('helloWORLD')  # 'HelloWORLD'
        """
        words = StrCase._split_into_words(value)
        return ''.join(word[0].upper() + word[1:] for word in words)
    
    @staticmethod
    def limit(value: str, limit: int = 100, end: str = '...') -> str:
        """
        Limite une chaîne à un nombre de caractères.
        
        Example:
            StrCase.limit('This is a long text', 7)  # 'This is...'
            StrCase.limit('Hello', 10)  # 'Hello'
            StrCase.limit('Too long', 5, '>')  # 'Too l>'
        """
        if len(value) <= limit:
            return value
        return value[:limit - len(end)] + end
    
    @staticmethod
    def contains(haystack: str, needles: str | list) -> bool:
        """
        Vérifie si une chaîne contient une ou plusieurs sous-chaînes.
        
        Example:
            StrCase.contains('Hello World', 'World')  # True
            StrCase.contains('Hello World', ['Hello', 'Nope'])  # True
            StrCase.contains('Hello World', ['Nope', 'Never'])  # False
        """
        if isinstance(needles, str):
            needles = [needles]
        return any(needle in haystack for needle in needles)
    
    @staticmethod
    def between(value: str, start: str, end: str) -> str:
        """
        Extrait une sous-chaîne entre deux chaînes.
        
        Example:
            StrCase.between('abc[def]ghi', '[', ']')  # 'def'
            StrCase.between('<div>content</div>', '<div>', '</div>')  # 'content'
        """
        start_pos = value.find(start)
        if start_pos == -1:
            return ''
        
        start_pos += len(start)
        end_pos = value.find(end, start_pos)
        if end_pos == -1:
            return ''
            
        return value[start_pos:end_pos]
    
    @staticmethod
    def after(value: str, search: str) -> str:
        """
        Retourne tout ce qui suit une chaîne donnée.
        
        Example:
            StrCase.after('hello/world', '/')  # 'world'
            StrCase.after('hello/world/test', '/')  # 'world/test'
        """
        pos = value.find(search)
        if pos == -1:
            return value
        return value[pos + len(search):]
    
    @staticmethod
    def before(value: str, search: str) -> str:
        """
        Retourne tout ce qui précède une chaîne donnée.
        
        Example:
            StrCase.before('hello/world', '/')  # 'hello'
            StrCase.before('hello/world/test', '/')  # 'hello'
        """
        pos = value.find(search)
        if pos == -1:
            return value
        return value[:pos]
    
    @staticmethod
    def wrap(value: str, before: str, after: Optional[str] = None) -> str:
        """
        Entoure une chaîne avec d'autres chaînes.
        
        Example:
            StrCase.wrap('hello', '*')  # '*hello*'
            StrCase.wrap('hello', '[', ']')  # '[hello]'
        """
        after = after or before
        return f"{before}{value}{after}"

    @staticmethod
    def start(value: str, prefix: str) -> str:
        """
        Ajoute un préfixe à une chaîne si elle ne commence pas déjà par celui-ci.
        
        Example:
            StrCase.start('test', '/')  # '/test'
            StrCase.start('/test', '/')  # '/test'
        """
        if not value.startswith(prefix):
            return f"{prefix}{value}"
        return value

    @staticmethod
    def finish(value: str, cap: str) -> str:
        """
        Ajoute un suffixe à une chaîne si elle ne se termine pas déjà par celui-ci.
        
        Example:
            StrCase.finish('test', '/')  # 'test/'
            StrCase.finish('test/', '/')  # 'test/'
        """
        if not value.endswith(cap):
            return f"{value}{cap}"
        return value

    @staticmethod
    def is_uuid(value: str) -> bool:
        """
        Vérifie si une chaîne est un UUID valide.
        
        Example:
            StrCase.is_uuid('123e4567-e89b-12d3-a456-426614174000')  # True
            StrCase.is_uuid('not-uuid')  # False
        """
        import re
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, value.lower()))

    @staticmethod
    def mask(value: str, character: str = '*', index: int = 1, length: Optional[int] = None) -> str:
        """
        Masque une partie d'une chaîne.
        
        Example:
            StrCase.mask('hello@example.com', '*', 2)  # 'he***@example.com'
            StrCase.mask('4242424242424242', '*', -4, 8)  # '4242********4242'
        """
        if length is None:
            length = len(value) - abs(index)

        start = index if index >= 0 else len(value) + index
        segment = value[start:start + length]
        
        if segment:
            return f"{value[:start]}{character * len(segment)}{value[start + length:]}"
        return value

    @staticmethod
    def excerpt(text: str, phrase: str, options: dict = None) -> str:
        """
        Extrait un extrait d'un texte autour d'une phrase.
        
        Example:
            text = "This is a long text with some words in it"
            StrCase.excerpt(text, "long", {'radius': 5})  # '...is a long text...'
            StrCase.excerpt(text, "text", {'omission': '...', 'radius': 10})
            # '...a long text with some...'
        """
        options = options or {}
        radius = options.get('radius', 100)
        omission = options.get('omission', '...')

        if not phrase or phrase not in text:
            return text[:radius] + omission if len(text) > radius else text

        pos = text.lower().index(phrase.lower())
        start = max(0, pos - radius)
        end = min(len(text), pos + len(phrase) + radius)

        excerpt = text[start:end]
        
        if start > 0:
            excerpt = omission + excerpt
        if end < len(text):
            excerpt = excerpt + omission
            
        return excerpt

    @staticmethod
    def replace_array(search: str, replace: list, subject: str) -> str:
        """
        Remplace les occurrences d'une chaîne par des valeurs d'un tableau.
        
        Example:
            text = "? and ? and ?"
            replacements = ['a', 'b', 'c']
            StrCase.replace_array('?', replacements, text)  # "a and b and c"
        """
        for replacement in replace:
            pos = subject.find(search)
            if pos == -1:
                break
            subject = subject[:pos] + str(replacement) + subject[pos + len(search):]
        return subject

    @staticmethod
    def random(length: int = 16) -> str:
        """
        Génère une chaîne aléatoire.
        
        Example:
            StrCase.random()  # 'j2Hs9Q7kL5mN4p3R'
            StrCase.random(8)  # 'kJ8mP2nS'
        """
        import random
        import string
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def squish(value: str) -> str:
        """
        Supprime tous les espaces superflus d'une chaîne.
        
        Example:
            StrCase.squish('  hello   world  ')  # 'hello world'
            StrCase.squish('hello    world')  # 'hello world'
        """
        import re
        return ' '.join(word for word in re.split(r'\s+', value.strip()) if word) 
    

def string() -> StrCase:
    return StrCase