<script>
    import { onMount } from 'svelte';
    /**
     * @type {any[]}
     */
    let challenge_data =  [];
    /**
     * @type {any[]}
     */
    let member_data = [];

    async function get_challenge_data(){
        const challenge_response = await fetch("http://localhost:8000/challenges",
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then((challenge_response) => challenge_response.json())
            .then((data) => {
                // console.log(data);
                challenge_data = data;
                // challenge_data = [...challenge_data, data];
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            }
        );
    }

    async function get_member_data(){
        const member_response = await fetch("http://localhost:8000/members",
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then((member_response) => member_response.json())
            .then((data) => {
                // console.log(data);
                member_data = data;
                // member_data = [...member_data, data];
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            }
        );
    }

    onMount(async() => {
        get_challenge_data();
        get_member_data();
    });

    // generate id from random
    let next_id = (member_data.length + 1).toString();
    let new_member = {
        id: next_id,
        name: "",
        current_challenge: "",
        start_time: "",
        check_in_time: "",
    }

    function create_member() {
        console.log("Adding new member...");
        member_data = [...member_data, new_member];
        next_id = (member_data.length + 1).toString();
        new_member = {
            id: next_id,
            name: "",
            current_challenge: "",
            start_time: "",
            check_in_time: "",
        }
    }

    /**
     * @param {string} id
     */
    function update_time(id) {
        console.log("update_time for " + id);
        const mod_now = dayjs().add(30, "minute").format("HHmm");
        challenge_data = challenge_data.map((data) => {
            console.log(data);
            if (data.id === id) {
                console.log("match found");
                return {
                    ...data,
                    checkin_time: mod_now.toString(),
                };
            }
            return data;
        });
    }

    let new_challenge = {
        name: "",
    };

    function add_new_challenge() {
        console.log("Adding new challenge...");
        challenge_data = [...challenge_data, new_challenge];
        new_challenge = {
            name: "",
        };
    }

    async function assign_challenge() {
        console.log("Assigning challenge...");
        // web request to put to localhost:8000/challenges
        const member_response = await fetch("http://localhost:8000/challenges",
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                // body: JSON.stringify({""}),
            })
            .then((member_response) => member_response.json())
            .then((data) => {
                console.log(data);
                member_data = [...member_data, data];
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            }
        );
    }
</script>


<div class="container my-4">
    <div class="row justify-content-lg-center">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th scope="col">Member</th>
                                <th scope="col">Challenge</th>
                                <th scope="col">Start Time</th>
                                <th scope="col">Check-in Time</th>
                                <th scope="col">Checked in?</th>
                            </tr>
                        </thead>
                        <tbody id="challenge_content">
                            {#if challenge_data.length > 0}
                                {#each challenge_data as data}
                                    <tr>
                                        <td>{data.member}</td>
                                        <td>{data.name}</td>
                                        <td>{data.start_time}</td>
                                        <td>{data.checkin_time}</td>
                                        <td>
                                            <button
                                                class="btn btn-primary"
                                                on:click={() =>
                                                    update_time(data.id)}
                                                >Yes</button
                                            >
                                        </td>
                                    </tr>
                                {/each}
                            {:else}
                                <tr>
                                    <td colspan="5">No data found</td>
                                </tr>
                            {/if}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
<div class="container my-4">
    <div class="row justify-content-lg-center">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-body">
                    <div
                        class="accordion accordion-flush"
                        id="accordionFlushExample"
                    >
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button
                                    class="accordion-button collapsed"
                                    type="button"
                                    data-bs-toggle="collapse"
                                    data-bs-target="#flush-collapseOne"
                                    aria-expanded="false"
                                    aria-controls="flush-collapseOne"
                                >
                                    Assign member to challenge
                                </button>
                            </h2>
                            <div
                                id="flush-collapseOne"
                                class="accordion-collapse collapse"
                                data-bs-parent="#accordionFlushExample"
                            >
                                <div class="accordion-body">
                                    <form on:submit={assign_challenge}>
                                    <!-- <form action="/progress" method="POST"> -->
                                        <div class="mb-3">
                                            <select
                                                class="form-select"
                                                aria-label="Default select example"
                                                placeholder="Select member to assign"
                                                required
                                            >
                                                <option selected
                                                    >Select member to assign</option
                                                >
                                                {#each member_data as data}
                                                    <option value={data.name}
                                                        >{data.name}</option
                                                    >
                                                {/each}
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <select
                                                class="form-select"
                                                aria-label="Default select example"
                                                placeholder="Select challenge to assign"
                                                required
                                            >
                                                <option selected
                                                    >Select challenge to assign</option
                                                >
                                                {#each challenge_data as data}
                                                    <option value={data.name}
                                                        >{data.name}</option
                                                    >
                                                {/each}
                                            </select>
                                        </div>
                                        <div class="mb-3">
                                            <label
                                                for="end_time"
                                                class="form-label"
                                                >Start time</label
                                            >
                                            <input
                                                type="number"
                                                class="form-control"
                                                id="start_time"
                                                name="start_time"
                                            />
                                        </div>
                                        <button
                                            type="submit"
                                            class="btn btn-primary"
                                            >Submit</button
                                        >
                                    </form>
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button
                                    class="accordion-button collapsed"
                                    type="button"
                                    data-bs-toggle="collapse"
                                    data-bs-target="#flush-collapseTwo"
                                    aria-expanded="false"
                                    aria-controls="flush-collapseTwo"
                                >
                                    Add new challenge
                                </button>
                            </h2>
                            <div
                                id="flush-collapseTwo"
                                class="accordion-collapse collapse"
                                data-bs-parent="#accordionFlushExample"
                            >
                                <div class="accordion-body">
                                    <form on:submit={add_new_challenge}>
                                        <!-- <form action="/challenges" method="POST"> -->
                                        <div class="mb-3">
                                            <input
                                                type="text"
                                                class="form-control"
                                                id="challenge"
                                                name="challenge"
                                                placeholder="Challenge name"
                                                bind:value={new_challenge.name}
                                                required
                                            />
                                        </div>
                                        <button
                                            type="submit"
                                            class="btn btn-primary"
                                            >Submit</button
                                        >
                                    </form>
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button
                                    class="accordion-button collapsed"
                                    type="button"
                                    data-bs-toggle="collapse"
                                    data-bs-target="#flush-collapseThree"
                                    aria-expanded="false"
                                    aria-controls="flush-collapseThree"
                                >
                                    Add new member
                                </button>
                            </h2>
                            <div
                                id="flush-collapseThree"
                                class="accordion-collapse collapse"
                                data-bs-parent="#accordionFlushExample"
                            >
                                <div class="accordion-body">
                                    <form on:submit={create_member}>

                                    <!-- <form action="/members" method="POST"> -->
                                        <div class="mb-3">
                                            <input
                                                type="text"
                                                class="form-control"
                                                id="member_name"
                                                name="member_name"
                                                placeholder="Enter member name"
                                                bind:value={new_member.name}
                                                required
                                            />
                                        </div>
                                        <button
                                            type="submit"
                                            class="btn btn-primary"
                                            >Submit</button
                                        >
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
