import * as React from "react";
import {Lesson, Student} from "./Entities";

const base_url = "http://localhost:7139";

export class MainTable extends React.Component<{}, {
    isLoaded: boolean,
    poll_url: string,
    lessons: Lesson[],
    students: Student[],
    error: any
}> {
    constructor(props) {
        super(props);

        this.state = {
            isLoaded: false,

            poll_url: "",

            students: [],
            lessons: [],

            error: null
        }

        this.handleChangePollURL = this.handleChangePollURL.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChangePollURL = (event) => this.setState({poll_url: event.target.value});

    handleSubmit(event) {
        let substr_index = this.state.poll_url.indexOf("poll") + 4;
        let substr = this.state.poll_url.slice(substr_index);
        let poll_id = substr.split("_")[0];
        let owner_id = substr.split("_")[1];

        fetch(base_url + "/lessons?" + new URLSearchParams({
            "owner_id": owner_id,
            "poll_id": poll_id
        }),
            {
                mode: 'cors',
                headers: {
                    'Access-Control-Allow-Origin': '*'
                }
            })
            .then((response) => {
                return response.json();
            })
            .then((data: Lesson[]) => {
                this.setState({
                    lessons: data,
                })
            });

        this.setState({isLoaded: true});
    }

    componentDidMount() {
        if (this.state.students.length !== 0) return;

        fetch(base_url + "/students",
            {
                mode: 'cors',
                headers: {
                    'Access-Control-Allow-Origin': '*'
                }
            })
            .then((response) => {
                return response.json();
            })
            .then((data: Student[]) => {
                data.sort((el1, el2) => el1.name.localeCompare(el2.name))
                this.setState({
                    students: data,
                })
            });
    }

    render() {
        return <>
            <div className="container">
                <div className="is-max-desktop columns">
                    <div className="column">
                        <input className="input" value={this.state.poll_url}
                               onChange={this.handleChangePollURL}
                               placeholder="Ссылка на опрос"/>
                    </div>
                    <div className="column">
                        <input className="button" value="Применить" onClick={this.handleSubmit}/>
                    </div>
                </div>
            </div>


            <table className="table is-bordered is-striped is-narrow is-hoverable is-fullwidth">
                <thead>
                <th className={'has-text-centered'}>Студенты</th>
                {this.state.lessons.map(lesson => <th className={"has-text-centered"}>{lesson.name}</th>)}
                </thead>

                <tbody>
                {
                    this.state.students.map((student: Student) =>
                        <tr>
                            <td className={"has-text-left"}>{student.name}</td>
                            {this.state.lessons.map(lesson =>
                                <td>
                                    {lesson.student_ids.includes(student.vk_id) ?
                                        <span className="icon has-text-success">
                                            <i className="fas fa-check-square"></i>
                                        </span>
                                        :
                                        <span className="icon has-text-danger">
                                            <i className="fas fa-ban"></i>
                                        </span>
                                    }
                                </td>
                            )}
                        </tr>
                    )}
                </tbody>
            </table>
        </>;
    }
}