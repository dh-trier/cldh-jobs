#!/usr/bin/env python3

"""
Modul für das Generieren eines Timestamps.
"""

import datetime

def timestamp():
    """
    Generiert einen timestamp im Format: Tag-Monat-Jahr-Stunde-Minute-Sekunden-Mikrosekunden
    """
    timestamp = datetime.datetime.now().strftime('%d%m%y%H%M%S%f')   
    return timestamp
    
