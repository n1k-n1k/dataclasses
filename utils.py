def get_traceback(ex: Exception) -> str:
    """ Формирование строки трэйсбека из объекта исключения """
    import traceback
    traceback_str = ''.join(traceback.format_tb(ex.__traceback__))
    return traceback_str
