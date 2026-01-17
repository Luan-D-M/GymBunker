export const integerType = {
  type: Number,
  validate: {
    validator: Number.isInteger,
    message: '{VALUE} is not an integer value'
  }
};
