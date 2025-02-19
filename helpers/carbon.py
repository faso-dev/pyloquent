from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Tuple

class Carbon:
    """
    Helper pour la manipulation des dates.
    
    Example:
        # Création de dates
        Carbon.now()  # datetime actuelle
        Carbon.today()  # date actuelle à minuit
        
        # Manipulation
        Carbon.add_days(date, 5)
        Carbon.sub_months(date, 2)
        
        # Comparaison
        Carbon.is_future(date)
        Carbon.is_past(date)
    """
    
    @staticmethod
    def now(tz: Optional[timezone] = None) -> datetime:
        """
        Retourne la date et l'heure actuelles.
        
        Example:
            Carbon.now()  # 2024-01-20 15:30:45+00:00
            Carbon.now(timezone.utc)  # 2024-01-20 15:30:45+00:00
        """
        return datetime.now(tz or timezone.utc)
    
    @staticmethod
    def today(tz: Optional[timezone] = None) -> datetime:
        """
        Retourne la date actuelle à minuit.
        
        Example:
            Carbon.today()  # 2024-01-20 00:00:00+00:00
        """
        now = Carbon.now(tz)
        return now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def tomorrow(tz: Optional[timezone] = None) -> datetime:
        """
        Retourne la date de demain à minuit.
        
        Example:
            Carbon.tomorrow()  # 2024-01-21 00:00:00+00:00
        """
        return Carbon.today(tz) + timedelta(days=1)
    
    @staticmethod
    def yesterday(tz: Optional[timezone] = None) -> datetime:
        """
        Retourne la date d'hier à minuit.
        
        Example:
            Carbon.yesterday()  # 2024-01-19 00:00:00+00:00
        """
        return Carbon.today(tz) - timedelta(days=1)
    
    @staticmethod
    def parse(value: Union[str, datetime], format: Optional[str] = None) -> datetime:
        """
        Parse une chaîne en datetime.
        
        Example:
            Carbon.parse('2024-01-20')  # 2024-01-20 00:00:00+00:00
            Carbon.parse('20/01/2024', '%d/%m/%Y')  # 2024-01-20 00:00:00+00:00
        """
        if isinstance(value, datetime):
            return value
        if format:
            return datetime.strptime(value, format)
        return datetime.fromisoformat(value)
    
    @staticmethod
    def format(date: datetime, format: str = '%Y-%m-%d %H:%M:%S') -> str:
        """
        Formate une date en chaîne.
        
        Example:
            date = Carbon.now()
            Carbon.format(date, '%d/%m/%Y')  # '20/01/2024'
            Carbon.format(date, '%H:%M')  # '15:30'
        """
        return date.strftime(format)
    
    @staticmethod
    def is_future(date: datetime) -> bool:
        """
        Vérifie si une date est dans le futur.
        
        Example:
            Carbon.is_future(Carbon.tomorrow())  # True
            Carbon.is_future(Carbon.yesterday())  # False
        """
        return date > Carbon.now(date.tzinfo)
    
    @staticmethod
    def is_past(date: datetime) -> bool:
        """
        Vérifie si une date est dans le passé.
        
        Example:
            Carbon.is_past(Carbon.yesterday())  # True
            Carbon.is_past(Carbon.tomorrow())  # False
        """
        return date < Carbon.now(date.tzinfo)
    
    @staticmethod
    def diff_for_humans(
        date: datetime,
        other: Optional[datetime] = None,
        absolute: bool = False
    ) -> str:
        """
        Retourne une différence de dates lisible par l'humain.
        
        Example:
            date = Carbon.parse('2024-01-19 15:30:00')
            Carbon.diff_for_humans(date)  # '1 day ago'
            Carbon.diff_for_humans(date, absolute=True)  # '1 day'
        """
        other = other or Carbon.now(date.tzinfo)
        diff = other - date if other > date else date - other
        
        seconds = int(diff.total_seconds())
        
        if seconds < 60:
            unit = 'second'
            count = seconds
        elif seconds < 3600:
            unit = 'minute'
            count = seconds // 60
        elif seconds < 86400:
            unit = 'hour'
            count = seconds // 3600
        else:
            unit = 'day'
            count = seconds // 86400
            
        if count != 1:
            unit += 's'
            
        if absolute:
            return f"{count} {unit}"
            
        return f"{count} {unit} ago" if other > date else f"in {count} {unit}"
    
    @staticmethod
    def add_days(date: datetime, days: int) -> datetime:
        """
        Ajoute des jours à une date.
        
        Example:
            date = Carbon.today()
            Carbon.add_days(date, 5)  # date + 5 jours
        """
        return date + timedelta(days=days)
    
    @staticmethod
    def sub_days(date: datetime, days: int) -> datetime:
        """
        Soustrait des jours à une date.
        
        Example:
            date = Carbon.today()
            Carbon.sub_days(date, 5)  # date - 5 jours
        """
        return date - timedelta(days=days)
    
    @staticmethod
    def start_of_day(date: datetime) -> datetime:
        """
        Retourne le début du jour.
        
        Example:
            date = Carbon.now()  # 2024-01-20 15:30:45
            Carbon.start_of_day(date)  # 2024-01-20 00:00:00
        """
        return date.replace(hour=0, minute=0, second=0, microsecond=0)
    
    @staticmethod
    def end_of_day(date: datetime) -> datetime:
        """
        Retourne la fin du jour.
        
        Example:
            date = Carbon.now()  # 2024-01-20 15:30:45
            Carbon.end_of_day(date)  # 2024-01-20 23:59:59
        """
        return date.replace(hour=23, minute=59, second=59, microsecond=999999) 
    

def carbon() -> Carbon:
    return Carbon

def now() -> Carbon:
    return Carbon.now()

def today() -> Carbon:
    return Carbon.today()

def tomorrow() -> Carbon:
    return Carbon.tomorrow()

def yesterday() -> Carbon:
    return Carbon.yesterday()



