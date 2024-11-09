import unittest
import random

from src.logica.coleccion import Coleccion
from src.modelo.album import Album, Medio
from src.modelo.declarative_base import Session
from faker import Faker

class AlbumTestCase(unittest.TestCase):
   def test_prueba(self):
        self.assertEqual(1, 1)
      
   def setUp(self):
        '''Crea una colección para hacer las pruebas'''
        self.coleccion = Coleccion()

        '''Abre la sesión'''
        self.session = Session()

        '''Crea una isntancia de Faker'''
        self.data_factory = Faker()

        '''Se programa para que Faker cree los mismos datos cuando se ejecuta'''
        Faker.seed(1000)

        '''Genera 10 datos en data y creamos los álbumes'''
        self.data = []
        self.albumes = []
        self.medios = [Medio.CD, Medio.CASETE, Medio.DISCO]

        for i in range(0,10):
            self.data.append((
                self.data_factory.unique.name(),
                self.data_factory.random_int(1800,2021),
                self.data_factory.text(),
                random.choice(self.medios)))
            self.albumes.append(
                Album(
                    titulo = self.data[-1][0],
                    ano = self.data[-1][1],
                    descripcion = self.data[-1][2],
                    medio = self.data[-1][3],
                    canciones = []
                ))
            self.session.add(self.albumes[-1])


        '''Persiste los objetos
            En este setUp no se cierra la sesión para usar los albumes en las pruebas'''
        self.session.commit()
    
   def test_constructor(self):
        for album, dato in zip(self.albumes, self.data):
            self.assertEqual(album.titulo, dato[0])
            self.assertEqual(album.ano, dato[1])
            self.assertEqual(album.descripcion, dato[2])
            self.assertEqual(album.medio, dato[3])
            
   def tearDown(self):
        '''Abre la sesión'''
        self.session = Session()

        '''Consulta todos los álbumes'''
        busqueda = self.session.query(Album).all()

        '''Borra todos los álbumes'''
        for album in busqueda:
            self.session.delete(album)

        self.session.commit()
        self.session.close()
        
   def test_agregar_album(self):
        '''Prueba la adición de un álbum'''
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(1800, 2021), self.data_factory.text(), random.choice(self.medios)))

        resultado = self.coleccion.agregar_album(
            titulo = self.data[-1][0],
            anio = self.data[-1][1],
            descripcion = self.data[-1][2],
            medio = self.data[-1][3])
        self.assertEqual(resultado, True)
        
   def test_agregar_album_repetido(self):
        '''Prueba la adición de un álbum repetido en el setup'''
        resultado = self.coleccion.agregar_album(
            titulo = self.data[-1][0],
            anio = self.data[-1][1],
            descripcion = self.data[-1][2],
            medio = self.data[-1][3])
        self.assertNotEqual(resultado, True)
        
   def test_editar_album(self):
        '''Prueba la edición de dos álbumes'''
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(1800, 2021), self.data_factory.text(), random.choice(self.medios)))

        #Se cambia el título el primer álbum creado por uno que no existe
        resultado1 = self.coleccion.editar_album(
            album_id = 1,
            titulo = self.data[-1][0],
            anio = self.data[-1][1],
            descripcion = self.data[-1][2],
            medio = self.data[-1][3])

        #Se cambia el título del segundo álbum creado por uno que ya existe
        resultado2 = self.coleccion.editar_album(
            album_id = 2,
            titulo = self.data[-3][0],
            anio = self.data[-3][1],
            descripcion = self.data[-3][2],
            medio = self.data[-3][3])

        self.assertTrue(resultado1)
        self.assertFalse(resultado2)
    
   def test_albumes_iguales(self):
        '''Prueba si dos álbumes son la misma referencia a un objeto al recuperar un album del almacenamiento'''
        album_nuevo = self.albumes[0]
        album_recuperado = self.coleccion.dar_album_por_id(1)
        self.assertIs(album_nuevo, self.albumes[0])
        self.assertIsNot(album_recuperado, self.albumes[0])
        
   def test_elemento_en_conjunto(self):
        '''Prueba que un elemento se encuentre en un conjunto'''
        album_nuevo = Album(
                    titulo = self.data_factory.unique.name(),
                    ano = self.data_factory.random_int(1800, 2021),
                    descripcion = self.data_factory.text(),
                    medio = random.choice(self.medios),
                    canciones = []
                )

        album_existente = self.albumes[2]

        self.assertIn(album_existente, self.albumes)
        self.assertNotIn(album_nuevo, self.albumes)
        
   def test_instancia_clase(self):
        '''Prueba que un elemento sea de una clase'''
        self.assertIsInstance(self.albumes[0], Album)
        self.assertNotIsInstance(self.coleccion, Album)
        
   def test_verificar_almacenamiento_agregar_album(self):
        '''Verifica que al almacenar los datos queden guardados en la el almacenamiento'''
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(1800, 2021), self.data_factory.text(), random.choice(self.medios)))

        self.coleccion.agregar_album(
            titulo = self.data[-1][0],
            anio = self.data[-1][1],
            descripcion = self.data[-1][2],
            medio = self.data[-1][3])

        album = self.session.query(Album).filter(Album.titulo == self.data[-1][0] and Album.ano == self.data[-1][1]).first()

        self.assertEqual(album.titulo, self.data[-1][0])
        self.assertEqual(album.ano, self.data[-1][1])
        self.assertEqual(album.descripcion, self.data[-1][2])
        self.assertIn(album.medio, self.medios)