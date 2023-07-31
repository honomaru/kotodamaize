// API mocking
import { createServer } from 'miragejs';

export function makeServer() {
  let server = createServer({
    routes() {
      this.post('http://localhost:5000/api/endpoint', () => {
        return {
          text: 'Some Text',
          mp3Url: 'Some URL'
        }
      });
    }
  });

  return server;
}