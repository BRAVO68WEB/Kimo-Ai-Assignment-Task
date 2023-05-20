from .schemas import Course

__all__ = ("CourseRead")

class CourseRead(Course):
    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        return d