
# Optional MySQL driver shim: allows using PyMySQL as MySQLdb
try:
    import pymysql  # type: ignore
    pymysql.install_as_MySQLdb()
except Exception:
    pass



