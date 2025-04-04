<template>
  <v-container>
    <v-row
      class="fill-height"
      align="center"
      justify="center"
    >
      <v-col cols="12" sm="8" md="10">
        <v-card class="pa-5">
          <div v-if="isLoading">
            <v-card-title class="text-center">
              <v-progress-circular
                indeterminate
                color="primary"
                size="64"
              ></v-progress-circular>
            </v-card-title>
          </div>
          <div v-else>
            <div v-if="memberships.length">
              <v-card-title class="text-center">
                <h2 class="display-1">Membership Information</h2>
              </v-card-title>
              <v-card-text>
                <v-data-table
                  :headers="headers"
                  :items="memberships"
                  class="elevation-1"
                  hide-default-footer
                >
                  <template v-slot:item.start_date="{ item }">
                    {{ new Date(item.start_date).toLocaleDateString() }}
                  </template>
                  <template v-slot:item.end_date="{ item }">
                    {{ new Date(item.end_date).toLocaleDateString() }}
                  </template>
                </v-data-table>
              </v-card-text>
            </div>
            <div v-else>
              <v-card-title class="text-center">
                <h2 class="display-1">Create Membership</h2>
              </v-card-title>
              <v-card-text>
                <v-form @submit.prevent="createMembership">
                  <v-select
                    v-model="membership_type"
                    :items="membershipTypes"
                    label="Membership Type"
                    required
                    class="mb-3"
                  ></v-select>
                  <v-text-field
                    v-model="start_date"
                    label="Start Date"
                    type="date"
                    required
                    class="mb-3"
                  ></v-text-field>
                  <v-text-field
                    v-model="end_date"
                    label="End Date"
                    type="date"
                    required
                    class="mb-4"
                  ></v-text-field>
                  <v-btn type="submit" color="primary" block large>
                    Create
                  </v-btn>
                </v-form>
              </v-card-text>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Membership',
  data() {
    return {
      isLoading: true,
      memberships: [],
      membership_type: '',
      start_date: '',
      end_date: '',
      membershipTypes: ['monthly', 'annually'],
      headers: [
        { title: 'ID', key: 'id' },
        { title: 'Membership Type', key: 'membership_type' },
        { title: 'Start Date', key: 'start_date' },
        { title: 'End Date', key: 'end_date' },
        { title: 'Active', key: 'active' }
      ]
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.$router.push({ name: 'Login' });
      return;
    }
    try {
      const response = await axios.get('http://localhost:5000/api/v1/memberships', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      this.memberships = response.data;
      console.log(this.memberships)
    } catch (error) {
      console.log('No memberships found.', error);
    } finally {
      this.isLoading = false;
    }
  },
  methods: {
    async createMembership() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.$router.push({ name: 'Login' });
        return;
      }

      try {
        await axios.post('http://localhost:5000/api/v1/memberships', {
          membership_type: this.membership_type,
          start_date: this.start_date,
          end_date: this.end_date
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        // Reload the memberships to reflect the newly created one
        this.created();
      } catch (error) {
        alert('Failed to create membership');
      }
    }
  }
};
</script>

<style>
html, body, #app, .v-application {
  height: 100%;
  margin: 0;
}
.fill-height {
  height: 100%;
}
.mb-3 {
  margin-bottom: 1rem;
}
.mb-4 {
  margin-bottom: 1.5rem;
}
</style>
