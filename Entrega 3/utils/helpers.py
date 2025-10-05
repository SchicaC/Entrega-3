def get_widgets_from_frame(frame):
    """Obtiene todos los widgets de un frame para limpieza"""
    widgets = []
    for child in frame.winfo_children():
        widgets.append(child)
        if hasattr(child, 'winfo_children'):
            widgets.extend(get_widgets_from_frame(child))
    return widgets