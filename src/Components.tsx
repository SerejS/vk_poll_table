import * as React from "react";

let subjects = [
    "Программирование",
    "АиГ",
    "Информатика",
    "Колпаков",
    "Анализ",
    "История",
];

class Student {
    private vk_id: Number;
    public name: string;

    constructor(vk_id: Number, name: string) {
        this.vk_id = vk_id;
        this.name = name;
    }

}

const students: Student[] = [
    new Student(364977556, "Соколов"),
    new Student(350738902, "Мавликаев"),
    new Student(212961717, "Рыжиков"),
    new Student(438049849, "Ильясов"),
    new Student(216533425, "Комосский"),
    new Student(736068632, "Слабнова"),
    new Student(413517083, "Шляхтин"),
    new Student(440597916, "Богатов"),
    new Student(132042348, "Долотов"),
    new Student(357468734, "Тищенко"),
    new Student(446496982, "Потапова"),
    new Student(289794276, "Малюская"),
    new Student(140725073, "Лисицкий"),
    new Student(408071406, "Двиков"),
    new Student(467091042, "Аникина"),
    new Student(465951261, "Маленковская"),
    new Student(459432773, "Заметаев"),
    new Student(156299873, "Газукина"),
    new Student(292074142, "Зазуля"),
    new Student(296380826, "Кузнецов"),
    new Student(183568418, "Фомина"),
    new Student(402681829, "Кривов"),
].sort((el1, el2) => el1.name.localeCompare(el2.name));

const Head: React.FC = () => {
    return (<thead>
    <th className={'has-text-centered'}>Студенты</th>
    {subjects.map(element => <th className={"has-text-centered"}>{element}</th>)}
    </thead>);
}

const Body: React.FC = () => {
    return (
        <tbody>

        {students.map((student: Student) => <tr>
            <td className={"has-text-left"}>{student.name}</td>
            {subjects.map(() =>
                <td>
                    {
                        Math.floor(Math.random() * 10) % 2 === 0 ?
                            <span className="icon has-text-success">
                                        <i className="fas fa-check-square"></i>
                                    </span>
                            :
                            <span className="icon has-text-danger">
                                        <i className="fas fa-ban"></i>
                                    </span>
                    }
                </td>)}
        </tr>)}
        </tbody>
    )
}


const MainTable: React.FC = () => {
    return (
        <>
            <table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                <Head/>
                <Body/>
            </table>
        </>
    );
}

export default MainTable;