# File for talking to database
#
import psycopg2

# docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
conn = psycopg2.connect(
    dbname="postgres", user="postgres", host="127.0.0.1", port=5432, password="abc"
)

# cursor = conn.cursor()
# cursor.execute('''CREATE TABLE mytable(
#     id int
# );''')

# cursor.execute('''insert into mytable values (4);''')
# cursor.execute('''select * from mytable;''')
# for i, record in enumerate(cursor):
#     print ("\n", type(record))
#     print ( record )
# cursor.close()
# conn.close()


def put_in_db(course, lecture, keywords, wp_pages, categories):
    query = """update lectures set keywords=%s, wp_pages=%s, categories=%s
    where course_code=%s and lecture_num=%s;"""
    cursor = conn.cursor()
    cursor.execute(query, (keywords, wp_pages, categories, course.course, lecture.num))
    cursor.close()


def dump_parsr_result(course, lecture, json_obj):
    query = """insert into lectures(course_code, lecture_num, parsr_json) values (%s, %s, %s);"""
    cursor = conn.cursor()
    cursor.execute(query, (course.course, lecture.num, json_obj,))
    cursor.close()


def get_parsed_json(course, lecture):
    # Check the DB to see if we've already got JSON parsed
    query = """select parsr_json from lectures where lecture_num = %s and course_code = %s;"""
    cursor = conn.cursor()
    cursor.execute(query, (lecture.num, course.course))
    row = cursor.fetchone()
    cursor.close()
    return row
    # if cursor.rowcount == 0:
    #     cursor.close()  # TODO: Do I close before fetching or after? after makes more sense tbh
    #     return None
    # cursor.close()  # TODO: Do I close before fetching or after? after makes more sense tbh
    # return cursor.fetchone()[0]


def has_parsed_result(course, lecture) -> bool:
    # check if keywords/wp-pages/categories
    query = (
        """select keywords from lectures where lecture_num = %s and course_code = %s;"""
    )
    cursor = conn.cursor()
    cursor.execute(query, (lecture.num, course.course))
    row = cursor.fetchone()
    cursor.close()
    return row[0] is not None

def close_connection():
    conn.commit()
    conn.close() # Probably need to wrap this ina  class. Instantiate just before calling db...