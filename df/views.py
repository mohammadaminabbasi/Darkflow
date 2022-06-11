from df.DFResponse import DFResponse


def home(request):
    return DFResponse(message="Home12", is_successful=True)
