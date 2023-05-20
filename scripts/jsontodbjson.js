const fs = require('fs')

const json = JSON.parse(fs.readFileSync('data/courses.json', 'utf8'))

const dbjson = json.map((course) => {
    course["course_id"] = Math.floor(Math.random() * 1000000)
    course["rating"] = Math.floor(Math.random() * 5) + 1
    course["no_of_ratings"] = Math.floor(Math.random() * 100) + 1
    course.chapters.forEach(element => {
        element["chapter_id"] = Math.floor(Math.random() * 1000000)
        element["rating"] = Math.floor(Math.random() * 5) + 1
        element["no_of_ratings"] = Math.floor(Math.random() * 100) + 1
        return element
    });
    return course
})

fs.writeFileSync('data/db.json', JSON.stringify(dbjson))