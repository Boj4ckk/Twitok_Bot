

class Clip:
    def __init__(self, id, title, duration, category, streamDate ,url ,views=0):
        """
        Initialise un clip vidéo.=
        :param id: l'identifiant du clip.
        :param title: Le titre du clip.
        :param duration: La durée du clip en secondes.
        :param views: Le nombre de vues du clip (par défaut 0).
        :param category: La catégorie du clip (gaming just chating etc..)
        :param StreamDate: La date du clip twitch
        :param url: L'URL du clip.

        """
        self.id = id 
        self.title = title
        self.duration = duration
        self.views = views
        self.category = category
        self.streamDate = streamDate
        self.url = url
    

    def getClipInfo(self):
        """
        Retourne un résumé des informations du clip.
        
        :return: Un dictionnaire contenant les informations du clip.
        """
        return {
            "id" : self.id,
            "title": self.title,
            "duration": self.duration,
            "views" : self.views,
            "category" : self.category,
            "streamDate" : self.streamDate,
            "url":  self.url,
            
            
        }
    

        
        


       
        
        
        




