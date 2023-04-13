<script>
    import { onMount } from "svelte";
    /**
     * @type {any[]}
     */
    $: challenge_data = [];

    /**
     * @type {any[]}
     */
    let member_data = [];

    async function get_challenge_data() {
        const challenge_response = await fetch(
            "http://localhost:8000/challenges",
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
            .then((challenge_response) => challenge_response.json())
            .then((data) => {
                console.log(data);
                challenge_data = data;
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            });
    }

    async function get_member_data() {
        const member_response = await fetch("http://localhost:8000/members", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((member_response) => member_response.json())
            .then((data) => {
                member_data = data;
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            });
    }

    onMount(async () => {
        get_challenge_data();
        get_member_data();
    });

    let new_member = {
        name: "",
    };

    async function create_member() {
        console.log("Adding new member...");
        //
        const create_member_response = await fetch(
            "http://localhost:8000/members",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(new_member),
            }
        )
            .then((create_member_response) => create_member_response.json())
            .then((data) => {
                get_member_data();
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            });
        new_member = {
            name: "",
        };
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

    async function add_new_challenge() {
        console.log("Adding new challenge...");
        const create_response = await fetch(
            "http://localhost:8000/challenges",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(new_challenge),
            }
        )
            .then((create_response) => create_response.json())
            .then((data) => {
                get_challenge_data();
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            }
        )
        new_challenge = {
            name: "",
        };
    }

    
    /**
     * @param {any} challenge_data
     */
    async function assign_challenge(challenge_data) {
        console.log(challenge_data);
        console.log("Assigning challenge...");
        const assign_response = await fetch(
            "http://localhost:8000/challenges",
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(challenge_data),
            }
        )
            .then((assign_response) => assign_response.json())
            .then((data) => {
                get_challenge_data();
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            });
    }

    /**
     * @param {any} challenge_data
     */
    async function complete_challenge(challenge_data) {
        console.log(challenge_data);
        challenge_data.completed = true;
        console.log("Completing challenge...");
        const complete_response = await fetch(
            "http://localhost:8000/challenges",
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(challenge_data),
            }
        )
            .then((complete_response) => complete_response.json())
            .then((data) => {
                get_challenge_data();
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("Error: " + error);
            });
    };
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
                                <th scope="col">Completed</th>
                            </tr>
                        </thead>
                        <tbody id="challenge_content">
                            {#if challenge_data.length > 0}
                                {#each challenge_data as challenge}
                                    {#if !challenge.completed}
                                    <tr>
                                        <td>
                                            <select
                                                class="form-select"
                                                aria-label="Default select example"
                                                placeholder="Select member to assign"
                                                required
                                                bind:value={challenge.member}
                                                on:change={() => assign_challenge(challenge)}
                                            >
                                                {#each member_data as member}
                                                    <option value={member.name}
                                                        >{member.name}</option
                                                    >
                                                {/each}
                                            </select>
                                        </td>
                                        <td>{challenge.name}</td>
                                        <td>{challenge.start_time}</td>
                                        <td>{challenge.checkin_time}</td>
                                        <td>
                                            <button
                                                class="btn btn-primary"
                                                on:click={() =>
                                                    update_time(challenge.id)}
                                                >Yes</button
                                            >
                                        </td>
                                        <td>
                                            <button
                                                class="btn btn-success"
                                                on:click={() =>
                                                    complete_challenge(challenge)}
                                                >Yes</button
                                            >
                                    </tr>
                                    {/if}
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
                    id="accordionCompletedChallenges"
                >
                    
                    <div class="accordion-item">
                        <h2 class="accordion-header">
                            <button
                                class="accordion-button collapsed"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#flush-collapseCompleted"
                                aria-expanded="false"
                                aria-controls="flush-collapseCompleted"
                            >
                                Completed Challenges
                            </button>
                        </h2>
                    </div>
                </div>
                <div
                    id="flush-collapseCompleted"
                    class="accordion-collapse collapse"
                    data-bs-parent="#accordionCompletedChallenges"
                >
                    <div class="accordion-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th scope="col">Member</th>
                                    <th scope="col">Challenge</th>
                                </tr>
                            </thead>
                            <tbody id="challenge_content">
                                {#if challenge_data.length > 0}
                                    {#each challenge_data as challenge}
                                        {#if challenge.completed}
                                            <tr>
                                                <td>{challenge.member}</td>
                                                <td>{challenge.name}</td>
                                            </tr>
                                        {/if}
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
                        <!-- <div class="accordion-item">
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
                        </div> -->
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
                                    Challenges
                                </button>
                            </h2>
                            <div
                                id="flush-collapseTwo"
                                class="accordion-collapse collapse"
                                data-bs-parent="#accordionFlushExample"
                            >
                                <div class="accordion-body">
                                    <form
                                        on:submit={add_new_challenge}
                                        class="input-group"
                                    >
                                        <input
                                            type="text"
                                            class="form-control"
                                            id="challenge"
                                            name="challenge"
                                            placeholder="Add new challenge"
                                            bind:value={new_challenge.name}
                                            required
                                        />
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
                                    Members
                                </button>
                            </h2>
                            <div
                                id="flush-collapseThree"
                                class="accordion-collapse collapse"
                                data-bs-parent="#accordionFlushExample"
                            >
                                <div class="accordion-body">
                                    <form on:submit={create_member} class="input-group mb-3">
                                        <input
                                            type="text"
                                            class="form-control"
                                            id="member_name"
                                            name="member_name"
                                            placeholder="Add a new member"
                                            bind:value={new_member.name}
                                            required
                                        />
                                        <button
                                            type="submit"
                                            class="btn btn-primary"
                                            >Submit</button
                                        >
                                    </form>

                                    <!-- <form on:submit={create_member} class="input-group">
                                        <input
                                            type="text"
                                            class="form-control"
                                            id="member_name"
                                            name="member_name"
                                            placeholder="Delete a member"
                                            bind:value={new_member.name}
                                            required
                                        />
                                        <button
                                            type="submit"
                                            class="btn btn-primary"
                                            >Submit</button
                                        >
                                    </form> -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
