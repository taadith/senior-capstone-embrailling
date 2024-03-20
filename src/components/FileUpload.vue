<template>
  <div>
    <input type="file" @change="handleFileUpload">
    <button @click="fileUpload">Upload</button>
    <div v-if="uploadedFileUrl">Uploaded File URL: {{ uploadedFileUrl }}</div>
    <p v-if=success class="success"> Success! </p>
    <p v-if=fail class="fail"> Fail! </p>
  </div>
</template>

<script>
import { uploadData } from 'aws-amplify/storage';
export default {
  data() {
    return {
      file: null,
      uploadedFileUrl: null,
      success: false,
      fail: false
    };
  },
  methods: {

  
    handleFileUpload(event) {
      this.success = false;
      this.fail = false;
      this.file = event.target.files[0];
    },

    async fileUpload(){
      try{
        const result = await uploadData({
          key: this.file.name,
          data: this.file,
          options:{
            accessLevel: 'guest',
          }
        }).result;
        console.log('Succeeded: ',result);
        this.success = true;
      }catch(error){
        console.log('Error: ',error);
      }
    }
  
  }
};
</script>

<style scoped>

.success{
  padding: 5px 10px;
  border: 2px solid green;
  color: white;
  background-color: green;
  border-radius: 5px;
}

.fail{
    padding: 5px 10px;
  border: 2px solid red;
  color: white;
  background-color: red;
  border-radius: 5px;
}


</style>

