<template>
    <v-form v-model="valid">
        <slot name="form"></slot>

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
</template>

<script>
    export default {
        name: 'LogTemplate',
        props: {
            id: {
                type: String
            },
            form: {
                type: Object
            }
        },
        data() {
            return {
                valid: false,
                pending: false
            }
        },
        methods: {
            submitForm() {
                if (!this.valid) {
                    return;
                }

                this.pending = true;

                fetch(`http://localhost:8000/api/forms/${this.id}`, {
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
