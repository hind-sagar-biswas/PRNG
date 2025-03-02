
const n = parseInt(process.argv[2]);
if (isNaN(n)) {
  console.error('Usage: node script.js n');
  process.exit(1);
}

let numbers = [];
for (let i = 0; i < n; i++) {
  numbers.push(Math.random());
}
console.log(numbers.join(' '));
