<template>
    <div class="event-participation pa-4">
        <v-card elevation="2">
            <v-card-text>
                <h4 class="text-h4 mb-4">Participation in Events</h4>

                <v-form
                        v-model="valid">
                    <v-select
                            :items="['Conference', 'Seminar',  'Workshop', 'Short Course', 'Other']"
                            v-model="form.eventType"

                            :rules="[
                                        v => !!v || 'Event type is required',
                                    ]"
                            required

                            label="Type of Event"
                    ></v-select>

                    <v-select
                            :items="['Invited Talk', 'Talk', 'Poster', 'No Communication']"
                            v-model="form.participationType"

                            :rules="[
                                        v => !!v || 'Participation type is required',
                                    ]"
                            required

                            label="Type of Participation"
                    ></v-select>

                    <v-text-field
                            v-model="form.title"

                            label="Title (if applicable)"
                    ></v-text-field>

                    <v-text-field
                            v-model="form.event"
                            :rules="[
                                        v => !!v || 'Event is required',
                                    ]"
                            required

                            label="Event"
                    ></v-text-field>

                    <v-text-field
                            v-model="form.local"
                            :rules="[
                                        v => !!v || 'Local is required',
                                    ]"
                            required

                            label="Local"
                    ></v-text-field>

                    <v-menu
                            :close-on-content-click="false"
                            transition="scale-transition"
                            offset-y
                            min-width="auto"
                    >
                        <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                                    :value="formatDate"
                                    label="Date"
                                    readonly
                                    v-bind="attrs"
                                    v-on="on"
                            ></v-text-field>
                        </template>
                        <v-date-picker
                                v-model="form.date"
                                range
                        ></v-date-picker>
                    </v-menu>

                    <v-textarea
                            v-model="form.observations"
                            solo

                            name="input-7-4"
                            label="Observations"
                    ></v-textarea>

                    <v-btn
                            :disabled="pending"
                            type="submit"
                            color="success"
                            outlined

                            @click.prevent="submitForm"
                    >
                        Submit
                    </v-btn>
                </v-form>
            </v-card-text>
        </v-card>
    </div>
</template>

<script>
    export default {
        name: 'EventParticipation',
        data() {
            return {
                valid: false,
                pending: false,
                form: {
                    eventType: '',
                    participationType: '',
                    title: '',
                    event: '',
                    local: '',
                    date: [new Date().toISOString().substr(0, 10), new Date().toISOString().substr(0, 10)],
                    observations: '',
                }
            }
        },
        computed: {
            formatDate() {
                return this.form.date.join(' ~ ')
            }
        },
        methods: {
            submitForm() {
                if (!this.valid) {
                    return;
                }

                this.pending = true;

                fetch(`http://localhost:8000/api/forms/event-participation`, {
                    method: "POST",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem("jwt")}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.form)
                })
                    .then(async response => {
                        const data = await response.json();

                        // check for error response
                        if (!response.ok) {
                            // get error message from body or default to response status
                            const error = (data && data.detail) || response.status;
                            return Promise.reject(error);
                        }

                        console.log(data)
                    })
                    .catch(error => {
                        console.log(error);
                    })
                    .finally(() => {
                        this.pending = false
                    });
            }
        }
    }
</script>
