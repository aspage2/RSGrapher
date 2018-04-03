class DragHandler:
    """Responsible for enabling plot labels to be dragged to a new location"""
    def __init__(self, canvas, callback, labels=None):
        self._labels = labels if labels is not None else []
        self._canvas = canvas
        self._callback = callback
        self._cids = (canvas.mpl_connect("button_press_event", self._press),
                      canvas.mpl_connect("button_release_event", self._release),
                      canvas.mpl_connect("motion_notify_event", self._move))

        self._drag_data = None  # (label_id, dx, dy)
        self._bg = None

    def __del__(self):
        for cid in self._cids:
            self._canvas.mpl_disconnect(cid)

    def _press(self, event):
        if event.inaxes is None:
            return

        for id, label in self._labels:
            c, a = label.contains(event)
            if c:
                x, y = label.get_position()
                self._drag_data = (id, label, x - event.xdata, y - event.ydata)
                label.set_animated(True)
                axes = self._canvas.axes
                self._canvas.draw()
                self._bg = self._canvas.copy_from_bbox(axes.bbox)
                axes.draw_artist(label)
                self._canvas.blit(axes.bbox)
                return

    def _move(self, event):
        if event.inaxes is None or self._drag_data is None:
            return
        id, label, dx, dy = self._drag_data
        label.set_position((event.xdata + dx, event.ydata + dy))

        axes = self._canvas.axes
        self._canvas.restore_region(self._bg)
        axes.draw_artist(label)
        self._canvas.blit(axes.bbox)

    def _release(self, event):
        if event.inaxes is None or self._drag_data is None:
            return
        id, label, dx, dy = self._drag_data
        self._bg = None
        label.set_animated(False)
        self._drag_data = None

        self._callback(id, label)

    def watch_label(self, label_id, label_obj):
        self._labels.append((label_id, label_obj))

    def ignore_label(self, label_id):
        for id, obj in self._labels:
            if id == label_id:
                self._labels.remove((id, obj))
                return
