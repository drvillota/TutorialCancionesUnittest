import unittest
import secrets

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

        '''Crea una instancia de Faker'''
        self.data_factory = Faker()

        '''Se programa para que Faker cree los mismos datos cuando se ejecuta'''
        Faker.seed(1000)

        '''Genera 10 datos en data y crea los álbumes'''
        self.data = []
        self.albumes = []
        self.medios = [Medio.CD, Medio.CASETE, Medio.DISCO]

        for _ in range(10):
            self.data.append((
                self.data_factory.unique.name(),
                self.data_factory.random_int(1800, 2021),
                self.data_factory.text(),
                secrets.choice(self.medios)
            ))
            self.albumes.append(
                Album(
                    titulo=self.data[-1][0],
                    ano=self.data[-1][1],
                    descripcion=self.data[-1][2],
                    medio=self.data[-1][3],
                    canciones=[]
                )
            )
            self.session.add(self.albumes[-1])

        '''Persiste los objetos'''
        self.session.commit()
    
    def test_constructor(self):
        for album, dato in zip(self.albumes, self.data):
            self.assertEqual(album.titulo, dato[0])
            self.assertEqual(album.ano, dato[1])
            self.assertEqual(album.descripcion, dato[2])
            self.assertEqual(album.medio, dato[3])
            
    def tearDown(self):
        '''Abre la sesión y borra todos los álbumes'''
        self.session = Session()
        busqueda = self.session.query(Album).all()
        for album in busqueda:
            self.session.delete(album)
        self.session.commit()
        self.session.close()
        
    def test_agregar_album(self):
        '''Prueba la adición de un álbum'''
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(1800, 2021), self.data_factory.text(), secrets.choice(self.medios)))

        resultado = self.coleccion.agregar_album(
            titulo=self.data[-1][0],
            anio=self.data[-1][1],
            descripcion=self.data[-1][2],
            medio=self.data[-1][3]
        )
        self.assertEqual(resultado, True)
        
    def test_agregar_album_repetido(self):
        '''Prueba la adición de un álbum repetido'''
        resultado = self.coleccion.agregar_album(
            titulo=self.data[-1][0],
            anio=self.data[-1][1],
            descripcion=self.data[-1][2],
            medio=self.data[-1][3]
        )
        self.assertNotEqual(resultado, True)
        
    def test_editar_album(self):
        '''Prueba la edición de dos álbumes'''
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(1800, 2021), self.data_factory.text(), secrets.choice(self.medios)))

        resultado1 = self.coleccion.editar_album(
            album_id=1,
            titulo=self.data[-1][0],
            anio=self.data[-1][1],
            descripcion=self.data[-1][2],
            medio=self.data[-1][3]
        )

        resultado2 = self.coleccion.editar_album(
            album_id=2,
            titulo=self.data[-3][0],
            anio=self.data[-3][1],
            descripcion=self.data[-3][2],
            medio=self.data[-3][3]
        )

        self.assertTrue(resultado1)
        self.assertFalse(resultado2)
    
    def test_albumes_iguales(self):
        '''Prueba si dos álbumes son la misma referencia a un objeto al recuperar un album'''
        album_nuevo = self.albumes[0]
        album_recuperado = self.coleccion.dar_album_por_id(1)
        self.assertIs(album_nuevo, self.albumes[0])
        self.assertIsNot(album_recuperado, self.albumes[0])
        
    def test_elemento_en_conjunto(self):
        '''Prueba que un elemento se encuentre en un conjunto'''
        album_nuevo = Album(
            titulo=self.data_factory.unique.name(),
            ano=self.data_factory.random_int(1800, 2021),
            descripcion=self.data_factory.text(),
            medio=secrets.choice(self.medios),
            canciones=[]
        )

        album_existente = self.albumes[2]

        self.assertIn(album_existente, self.albumes)
        self.assertNotIn(album_nuevo, self.albumes)
        
    def test_instancia_clase(self):
        '''Prueba que un elemento sea de una clase'''
        self.assertIsInstance(self.albumes[0], Album)
        self.assertNotIsInstance(self.coleccion, Album)
        
    def test_verificar_almacenamiento_agregar_album(self):
        '''Verifica que al almacenar los datos queden guardados en el almacenamiento'''
        self.data.append((self.data_factory.unique.name(), self.data_factory.random_int(1800, 2021), self.data_factory.text(), secrets.choice(self.medios)))

        self.coleccion.agregar_album(
            titulo=self.data[-1][0],
            anio=self.data[-1][1],
            descripcion=self.data[-1][2],
            medio=self.data[-1][3]
        )

        album = self.session.query(Album).filter(Album.titulo == self.data[-1][0]).first()

        self.assertEqual(album.titulo, self.data[-1][0])
        self.assertEqual(album.ano, self.data[-1][1])
        self.assertEqual(album.descripcion, self.data[-1][2])
        self.assertIn(album.medio, self.medios)
    
    def test_dar_album_por_id(self):
        '''Verifica la recuperación de un álbum por ID'''
        nuevo_album = Album(
            titulo="Álbum de prueba",
            ano=2020,
            descripcion="Descripción de prueba",
            medio=Medio.CD
        )
        self.session.add(nuevo_album)
        self.session.commit()

        album_recuperado = self.coleccion.dar_album_por_id(nuevo_album.id)
        
        self.assertEqual(album_recuperado['titulo'], "Álbum de prueba")
        self.assertEqual(album_recuperado['ano'], 2020)
        self.assertEqual(album_recuperado['descripcion'], "Descripción de prueba")
        self.assertEqual(album_recuperado['medio'], Medio.CD)

    def test_eliminar_album(self):
        '''Prueba la eliminación de un álbum'''
        # Agregar un nuevo álbum para eliminar
        nuevo_album = Album(
            titulo="Álbum a eliminar",
            ano=2021,
            descripcion="Álbum que será eliminado",
            medio=Medio.CASETE
        )
        self.session.add(nuevo_album)
        self.session.commit()

        album_id = nuevo_album.id
        resultado = self.coleccion.eliminar_album(album_id)
        
        self.assertTrue(resultado)

        # Verificar que el álbum ya no está en la base de datos
        album_eliminado = self.session.query(Album).filter(Album.id == album_id).first()
        self.assertIsNone(album_eliminado)