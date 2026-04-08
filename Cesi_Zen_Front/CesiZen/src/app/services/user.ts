import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class UserSrv {
  
  private users = [
    { id: 1, name: 'Alexis Le Dantec', email: 'alexis@example.com', age: 21 },
    { id: 2, name: 'Jane Smith', email: 'jane@example.com', age: 25 },
    { id: 3, name: 'Bob Johnson', email: 'bob@example.com', age: 35 },
  ];

  constructor() {}
  
  
  getUsers() {
    return this.users;
  }

  // private apiUrl = 'api/users';
  /*constructor(private http: HttpClient) {}

  getUsers() {
    return this.http.get<any[]>(this.apiUrl);
  }

  getUser(id: number) {
    return this.http.get<any>(`${this.apiUrl}/${id}`);
  }

  createUser(user: any) {
    return this.http.post<any>(this.apiUrl, user);
  }

  updateUser(id: number, user: any) {
    return this.http.put<any>(`${this.apiUrl}/${id}`, user);
  }

  deleteUser(id: number) {
    return this.http.delete<any>(`${this.apiUrl}/${id}`);
  } */


}
