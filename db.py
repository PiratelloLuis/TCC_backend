import sqlite3


class Database:
    def __init__(self, db_name='alunos.db'):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS aluno (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                nota INTEGER
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS perguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                texto TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS respostas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_pergunta INTEGER,
                id_aluno INTEGER,
                resposta TEXT NOT NULL,
                FOREIGN KEY (id_pergunta) REFERENCES perguntas(id),
                FOREIGN KEY (id_aluno) REFERENCES aluno(id)
            )
        ''')
        self.conn.commit()

    def inserir_aluno(self, nome):
        self.cursor.execute('''
            INSERT INTO aluno (nome) VALUES (?)
        ''', (nome,))
        self.conn.commit()
        return self.cursor.lastrowid

    def inserir_pergunta(self, pergunta):
        self.cursor.execute('''
            INSERT INTO perguntas (texto) VALUES (?)
        ''', (pergunta,))
        self.conn.commit()
        return self.cursor.lastrowid

    def inserir_resposta(self, id_pergunta, id_aluno, resposta):
        self.cursor.execute('''
            INSERT INTO respostas (id_pergunta, id_aluno, resposta) VALUES (?, ?, ?)
        ''', (id_pergunta, id_aluno, resposta))
        self.conn.commit()

    def atualizar_nota(self, id_aluno, nota):
        self.cursor.execute('''
            UPDATE aluno SET nota = ? WHERE id = ?
        ''', (nota, id_aluno))
        self.conn.commit()

    def listar_alunos(self):
        self.cursor.execute('SELECT * FROM aluno')
        return self.cursor.fetchall()

    def listar_perguntas(self):
        self.cursor.execute('SELECT * FROM perguntas')
        return self.cursor.fetchall()

    def listar_respostas(self):
        self.cursor.execute('SELECT * FROM respostas')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
