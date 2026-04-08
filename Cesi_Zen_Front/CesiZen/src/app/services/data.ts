import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class Data {
  private listFruits: string[] = ['papaye', 'ananas', 'kiwi', 'pamplemousse'];

  constructor() {
    console.log('Contructeur liste');
  }

  getListFruits() {
    return this.listFruits;
  }

  addFruit(fruit: string) {
    this.listFruits.push(fruit);
  }
  
  resetListFruits() {
    this.listFruits = [];
  }
}
